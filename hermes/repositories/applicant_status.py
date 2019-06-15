import asyncio
import datetime
from typing import Type, Dict, Any, Callable, Awaitable

from hermes.repositories.connections import DBConnection, CacheConnection


class ApplicantStatusPersistentRepository:
    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

        self._patch_receipt_code = self._get_patch_function("receipt_code")
        self._patch_is_paid = self._get_patch_function("is_paid")
        self._patch_is_printed_application_arrived = self._get_patch_function(
            "is_printed_application_arrived"
        )
        self._patch_is_passed_first_apply = self._get_patch_function("is_passed_first_apply")
        self._patch_is_final_submit = self._get_patch_function("is_final_submit")
        self._patch_exam_code = self._get_patch_function("exam_code")

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
            query = (
                f"UPDATE applicant_status SET {column} = %s, updated_at = %s WHERE applicant_email = %s"
            )

            await self.connection.execute(query, value, datetime.datetime.now(), email)

        return _patch_function

