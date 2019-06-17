import asyncio
import datetime
from typing import Any, Awaitable, Callable, Dict, Type

from hermes.repositories.connections import CacheConnection, DBConnection


class ApplicantStatusPersistentRepository:
    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

        self._patch_receipt_code = self._get_patch_function("receipt_code")
        self._patch_is_paid = self._get_patch_function("is_paid")
        self._patch_is_printed_application_arrived = self._get_patch_function(
            "is_printed_application_arrived"
        )
        self._patch_is_passed_first_apply = self._get_patch_function(
            "is_passed_first_apply"
        )
        self._patch_is_final_submit = self._get_patch_function("is_final_submit")
        self._patch_exam_code = self._get_patch_function("exam_code")

    table_creation_query = """
            create table if not exists applicant_status
            (
              applicant_email                varchar(320)                        not null
                primary key,
              receipt_code                   int(3) unsigned zerofill auto_increment,
              is_paid                        tinyint   default 0                 not null,
              is_printed_application_arrived tinyint   default 0                 not null,
              is_passed_first_apply          tinyint   default 0                 not null,
              is_final_submit                tinyint   default 0                 not null,
              exam_code                      varchar(6)                          null,
              created_at                     timestamp default CURRENT_TIMESTAMP not null,
              updated_at                     timestamp default CURRENT_TIMESTAMP not null,
              constraint exam_code_UNIQUE
                unique (exam_code),
              constraint receipt_code_UNIQUE
                unique (receipt_code),
              constraint fk_applicant_status_applicant
                foreign key (applicant_email) references applicant (email)
                  on update cascade on delete cascade
            ) character set utf8mb4;
        """

    async def init(self, email):
        query = "INSERT INTO applicant_status (applicant_email) VALUES (%s)"
        await self.connection.execute(query, email)

    async def patch(self, email: str, patch_data: Dict[str, Any]) -> None:
        tasks = list()
        patch_data = {k: v for k, v in patch_data.items() if v}

        for k, v in patch_data.items():
            task: Callable[[Type[DBConnection], str, str], Awaitable[None]] = getattr(
                self, f"_patch_{k}", None
            )

            if task:
                tasks.append(task(self.connection, email, v))

        await asyncio.gather(*tasks)

    async def get_one(self, email: str) -> Dict[str, Any]:
        query = """
            SELECT 
            applicant_email,
            receipt_code,
            is_paid,
            is_printed_application_arrived,
            is_passed_first_apply,
            is_final_submit,
            exam_code
            FROM applicant_status
            WHERE applicant_email = %s;
        """
        return await self.connection.fetchone(query, email)

    def _get_patch_function(self, column: str) -> Callable[[str, str], Awaitable[None]]:
        async def _patch_function(email: str, value: Any) -> None:
            query = f"UPDATE applicant_status SET {column} = %s, updated_at = %s WHERE applicant_email = %s"

            await self.connection.execute(query, value, datetime.datetime.now(), email)

        return _patch_function


class ApplicantStatusCacheRepository:
    _key_template: str = "hermes:applicant:status:{0}"

    def __init__(self, connection: Type[CacheConnection]):
        self.connection = connection

    async def set(self, applicant: Dict[str, Any]) -> None:
        await self.connection.set(
            self._key_template.format(applicant["applicant_email"]), applicant
        )

    async def get(self, email: str) -> Dict[str, Any]:
        return await self.connection.get(self._key_template.format(email))

    async def delete(self, email: str) -> None:
        return await self.connection.delete(self._key_template.format(email))
