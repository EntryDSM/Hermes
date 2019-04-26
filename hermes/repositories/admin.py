import asyncio
import datetime
from typing import Callable, Dict, Type, Optional, List, Any

from werkzeug.security import generate_password_hash

from hermes.repositories.connections import DBConnection, CacheConnection


class AdminPersistentRepository:
    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

    async def save(self, admin: Dict[str, Any]) -> None:
        query = """INSERT INTO admin (
                    admin_id,
                    admin_password,
                    admin_type,
                    admin_email,
                    admin_name
                    ) VALUES (%s, %s, %s, %s, %s)"""

        await self.connection.execute(
            query, admin["admin_id"],
            generate_password_hash(admin["admin_password"]),
            admin["admin_type"],
            admin["admin_email"],
            admin["admin_name"]
        )

    async def delete(self, admin_id: str) -> None:
        query = """
        DELETE FROM admin WHERE admin_id = %s ;
        """
        await self.connection.execute(query, admin_id)

    async def patch(self, admin_id: str, patch_data: Dict[str, Any]) -> None:
        tasks = list()

        for k, v in patch_data:
            task: Callable = self.__getattribute__(f"_patch_{k}")

            if task:
                tasks.append(task(admin_id, v))

        await asyncio.gather(*tasks)

    async def _patch_admin_type(self, admin_id: str, new_type: str) -> None:
        query = "UPDATE admin SET admin_type = %s, updated_at = %s, WHERE admin_id = %s ;"
        await self.connection.execute(query, new_type, datetime.datetime.now(), admin_id)

    async def _patch_admin_name(self, admin_id: str, new_name: str) -> None:
        query = "UPDATE admin SET admin_name = %s, updated_at = %s, WHERE admin_id = %s ;"
        await self.connection.execute(query, new_name, datetime.datetime.now(), admin_id)

    async def _patch_admin_email(self, admin_id: str, new_email: str) -> None:
        query = "UPDATE admin SET admin_email = %s, updated_at = %s, WHERE admin_id = %s ;"
        await self.connection.execute(query, new_email, datetime.datetime.now(), admin_id)

    async def get_list(self, filters: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
        query = "SELECT admin_id, admin_name, admin_password, admin_type, admin_email FROM admin "

        if filters:
            query += self._complete_where_statement(filters)

        return await self.connection.fetch(query, *filters.values())

    @classmethod
    def _complete_where_statement(cls, filters: Dict[str, str]) -> str:
        base_query = "WHERE"
        for k in filters:
            base_query += f" {k} = %s AND"

        return base_query[:-3] + ";"

    async def get_one(self, admin_id: str) -> Optional[Dict[str, str]]:
        query = "SELECT admin_id, admin_name, admin_password, admin_type, admin_email FROM admin WHERE admin_id = %s ;"

        return await self.connection.fetchone(query, admin_id)

