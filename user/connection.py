import os
import aiomysql
from typing import List, Dict, Any

from user.config import settings


READ_CONNECTION_INFO = {
    'use_unicode': True,
    'charset': 'utf8mb4',
    'user': settings.get_database_cred()[0],
    'password': settings.get_database_cred()[1],
    'db': settings.READ_MYSQL_DATABASE,
    'host': settings.READ_MYSQL_HOST,
    'port': settings.READ_MYSQL_PORT,
    'loop': None,
    'autocommit': True
}

WRITE_CONNECTION_INFO = {
    'use_unicode': True,
    'charset': 'utf8mb4',
    'user': settings.get_database_cred()[0],
    'password': settings.get_database_cred()[1],
    'db': settings.WRITE_MYSQL_DATABASE,
    'host': settings.WRITE_MYSQL_HOST,
    'port': settings.WRITE_MYSQL_PORT,
    'loop': None,
    'autocommit': True
}


class MySQLConnection:
    read_pool: aiomysql.Pool = None
    write_pool: aiomysql.Pool = None

    @staticmethod
    async def initialize(connection_info=None):
        await MySQLConnection.get_read_pool(connection_info)
        await MySQLConnection.get_write_pool(connection_info)

    @staticmethod
    async def destroy():
        if MySQLConnection.read_pool is not None:
            MySQLConnection.read_pool.close()
            await MySQLConnection.read_pool.wait_closed()
        if MySQLConnection.write_pool is not None:
            MySQLConnection.write_pool.close()
            await MySQLConnection.write_pool.wait_closed()

        MySQLConnection.read_pool = None
        MySQLConnection.write_pool = None

    @classmethod
    async def get_read_pool(cls, read_connection_info=None) -> aiomysql.Pool:
        if cls.read_pool and not cls.read_pool._closed:
            return cls.read_pool

        cls.read_pool = await aiomysql.create_pool(**read_connection_info) if read_connection_info \
            else await aiomysql.create_pool(**READ_CONNECTION_INFO)

        return cls.read_pool

    @classmethod
    async def get_write_pool(cls, write_connection_info=None) -> aiomysql.Pool:
        if cls.write_pool and not cls.write_pool._closed:
            return cls.write_pool

        cls.write_pool = await aiomysql.create_pool(**write_connection_info) if write_connection_info \
            else await aiomysql.create_pool(**WRITE_CONNECTION_INFO)

        return cls.write_pool

    @classmethod
    async def execute(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls.get_write_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: int

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await cur.execute(query, args)

        return result

    @classmethod
    async def executemany(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls.get_write_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: int

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await cur.executemany(query, args)

        return result

    @classmethod
    async def fetch(cls, query: str, *args) -> List[Dict[str, Any]]:
        pool: aiomysql.Pool = await cls.get_read_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: List[Dict[str, Any]]

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchall()

        return result

    @classmethod
    async def fetchone(cls, query: str, *args) -> Dict[str, Any]:
        pool: aiomysql.Pool = await cls.get_read_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: Dict[str, Any]

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchone()

        return result
