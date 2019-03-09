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

