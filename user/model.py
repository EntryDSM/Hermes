from typing import Dict, Union, Iterable, Tuple, List

from werkzeug.security import check_password_hash, generate_password_hash

from user.connection import MySQLConnection
from user.descriptor import *


class BaseModel:
    table_name: str
    indexes: Dict[str, Union[str, Tuple]]

    table_creation_statement: str

    @classmethod
    async def create_table(cls):
        await MySQLConnection.execute(cls.table_creation_statement)
        await cls.create_table_index()

    @classmethod
    async def create_table_index(cls):
        for index_name, index_key in cls.indexes.items():
            await MySQLConnection.execute(f"CREATE INDEX {index_name} ON {cls.table_name} ({', '.join(str(i) for i in index_key)})")

    async def save(self):
        pass


class Admin(BaseModel):
    table_name = "admin"
    indexes = {
        "type_index": ("admin_type", ),
        "name_index": ("admin_name", ),
    }

    table_creation_statement = f"""
        create table if not exists {table_name}
            (
              admin_id       varchar(45)                                  not null
                primary key,
              admin_password varchar(320)                                  not null,
              admin_type     enum ('ROOT', 'ADMINISTRATION', 'INTERVIEW') not null,
              admin_email    varchar(320)                                 not null,
              admin_name     varchar(13)                                  not null,
              created_at     timestamp default CURRENT_TIMESTAMP          not null,
              updated_at     timestamp default CURRENT_TIMESTAMP          not null
            ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;
    """

    admin_id = UUID(allow_none=False)
    admin_password = Password(allow_none=False)
    admin_type = AdminEnum(allow_none=False)
    admin_email = Email(allow_none=False)
    admin_name = String(length=13, allow_none=False)
    created_at = TimeStamp(default=datetime.datetime.now, allow_none=False)
    updated_at = TimeStamp(default=created_at, allow_none=False)

    def __init__(self, admin_name, admin_email, admin_password, admin_type, admin_id=None, created_at=None, updated_at=None):
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.admin_type = admin_type

        if created_at and updated_at and admin_id:
            self.admin_id = admin_id
            self.created_at = created_at
            self.updated_at = updated_at

    async def save(self):
        query = f"""INSERT INTO {self.table_name} (
                    admin_id,
                    admin_password,
                    admin_type,
                    admin_email,
                    admin_name,
                    created_at,
                    updated_at,
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        await MySQLConnection.execute(query, self.admin_id, generate_password_hash(self.admin_password),
                                      self.admin_type, self.admin_email, self.admin_name,
                                      self.created_at, self.updated_at)

    @classmethod
    async def query_by_email(cls, email: str) -> "Admin":
        query = f"""
                SELECT *
                FROM {cls.table_name}
                WHERE admin_email = %s
                """

        result = await MySQLConnection.fetchone(query, email)
        return Admin(**result) if result else None

    @classmethod
    async def query_by_name(cls, name: str) -> "Admin":
        query = f"""
        SELECT *
        FROM {cls.table_name}
        WHERE admin_name = %s
        """

        result = await MySQLConnection.fetchone(query, name)
        return Admin(**result) if result else None

    @classmethod
    async def get_type(cls, email: str) -> "Admin":
        query = f"""
                SELECT *
                FROM {cls.table_name}
                WHERE admin_email = %s
                """

        result = await MySQLConnection.fetchone(query, email)
        return result["admin_type"] if result else None


