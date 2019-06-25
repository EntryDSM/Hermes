import asyncio
import datetime
from typing import Any, Awaitable, Callable, Dict, List, Type

from werkzeug.security import generate_password_hash

from hermes.repositories.connections import CacheConnection, DBConnection


class ApplicantPersistentRepository:
    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

        self._patch_password = self._get_patch_function("password")
        self._patch_applicant_name = self._get_patch_function("applicant_name")
        self._patch_sex = self._get_patch_function("sex")
        self._patch_birth_date = self._get_patch_function("birth_date")
        self._patch_parent_name = self._get_patch_function("parent_name")
        self._patch_parent_tel = self._get_patch_function("parent_tel")
        self._patch_applicant_tel = self._get_patch_function("applicant_tel")
        self._patch_address = self._get_patch_function("address")
        self._patch_post_code = self._get_patch_function("post_code")

    table_creation_query = """
                create table if not exists applicant
                (
                  email          varchar(320)                        not null
                    primary key,
                  password       varchar(320)                        not null,
                  applicant_name varchar(13)                         null,
                  sex            enum ('MALE', 'FEMALE')             null,
                  birth_date     date                                null,
                  parent_name    varchar(13)                         null,
                  parent_tel     varchar(12)                         null,
                  applicant_tel  varchar(12)                         null,
                  address        varchar(500)                        null,
                  post_code      varchar(5)                          null,
                  image_path     varchar(256)                        null,
                  created_at     timestamp default CURRENT_TIMESTAMP not null,
                  updated_at     timestamp default CURRENT_TIMESTAMP not null,
                  constraint applicant_tel_UNIQUE
                    unique (applicant_tel),
                  constraint image_path_UNIQUE
                    unique (image_path)
                ) character set utf8mb4;
            """

    async def save(self, email: str, password: str):
        query = """INSERT INTO applicant (
                    email,
                    password
                    ) VALUES (%s, %s)"""

        await self.connection.execute(query, email, generate_password_hash(password))

    async def patch(self, email: str, patch_data: Dict[str, Any]) -> None:
        tasks = list()
        patch_data = {k: v for k, v in patch_data.items() if v}

        for k, v in patch_data.items():
            task: Callable[[Type[DBConnection], str, str], Awaitable[None]] = getattr(
                self, f"_patch_{k}", None
            )

            if task:
                tasks.append(task(email, v))

        await asyncio.gather(*tasks)

    async def get_one(self, email: str) -> Dict[str, str]:
        query = """
            SELECT 
            email,
            password,
            applicant_name, 
            sex, 
            birth_date, 
            parent_name,
            parent_tel, 
            applicant_tel,
            address, 
            post_code, 
            image_path 
            FROM applicant 
            WHERE email = %s
        """

        return await self.connection.fetchone(query, email)

    async def get_list(self, filters: Dict[str, str] = None) -> List[Dict[str, str]]:
        query = """
            SELECT 
            email,
            password,
            applicant_name, 
            sex, 
            birth_date, 
            parent_name,
            parent_tel, 
            applicant_tel,
            address, 
            post_code, 
            image_path 
            FROM applicant 
        """

        filters = {} if not filters else filters

        query += self._complete_where_statement(filters)
        return await self.connection.fetch(query, *filters.values())

    async def delete(self, email: str) -> None:
        query = "DELETE FROM applicant WHERE email = %s"

        await self.connection.execute(query, email)

    def _get_patch_function(self, column: str) -> Callable[[str, str], Awaitable[None]]:
        async def _patch_function(email: str, value: Any) -> None:
            query = (
                f"UPDATE applicant SET {column} = %s, updated_at = %s WHERE email = %s"
            )

            await self.connection.execute(query, value, datetime.datetime.now(), email)

        return _patch_function

    @classmethod
    def _complete_where_statement(cls, filters: Dict[str, str]) -> str:
        columns = ["email", "applicant_name", "sex"]

        base_query = "WHERE"
        for k in filters:
            if k not in columns:
                continue
            base_query += f" {k} = %s AND"

        return base_query[:-3] + ";"


class ApplicantCacheRepository:
    _key_template: str = "hermes:applicant:{0}"

    def __init__(self, connection: Type[CacheConnection]):
        self.connection = connection

    async def set(self, applicant: Dict[str, Any]) -> None:
        await self.connection.set(
            self._key_template.format(applicant["email"]), applicant
        )

    async def get(self, email: str) -> Dict[str, Any]:
        return await self.connection.get(self._key_template.format(email))

    async def delete(self, email: str) -> None:
        return await self.connection.delete(self._key_template.format(email))
