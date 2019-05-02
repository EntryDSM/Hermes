import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import aiomysql
import aioredis


class DBConnection(ABC):
    @classmethod
    @abstractmethod
    async def initialize(cls, connection_info):
        ...

    @classmethod
    @abstractmethod
    async def destroy(cls):
        ...

    @classmethod
    @abstractmethod
    async def execute(cls, query: str, *args) -> int:
        ...

    @classmethod
    @abstractmethod
    async def executemany(cls, query: str, *args) -> int:
        ...

    @classmethod
    @abstractmethod
    async def fetch(cls, query: str, *args) -> List[Dict[str, Any]]:
        ...

    @classmethod
    @abstractmethod
    async def fetchone(cls, query: str, *args) -> Dict[str, Any]:
        ...


class MySQLConnection(DBConnection):
    _read_pool: aiomysql.Pool = None
    _write_pool: aiomysql.Pool = None
    _connection_info = None

    @classmethod
    async def initialize(cls, connection_info):
        cls._connection_info = connection_info

        await cls._get_read_pool()
        await cls._get_write_pool()

    @classmethod
    async def destroy(cls):
        if cls._read_pool is not None:
            cls._read_pool.close()
            await cls._read_pool.wait_closed()
        if cls._write_pool is not None:
            cls._write_pool.close()
            await cls._write_pool.wait_closed()

        MySQLConnection._read_pool = None
        MySQLConnection._write_pool = None

    @classmethod
    async def _get_read_pool(cls) -> aiomysql.Pool:
        if cls._read_pool and not cls._read_pool._closed:  # pylint: disable=protected-access
            return cls._read_pool

        cls._read_pool = await aiomysql.create_pool(**cls._connection_info)

        return cls._read_pool

    @classmethod
    async def _get_write_pool(cls) -> aiomysql.Pool:
        if cls._write_pool and not cls._write_pool._closed:  # pylint: disable=protected-access
            return cls._write_pool

        cls._write_pool = await aiomysql.create_pool(**cls._connection_info)

        return cls._write_pool

    @classmethod
    async def execute(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_write_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: int

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await cur.execute(query, args)

        return result

    @classmethod
    async def executemany(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_write_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: int

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await cur.executemany(query, args)

        return result

    @classmethod
    async def fetch(cls, query: str, *args) -> List[Dict[str, Any]]:
        pool: aiomysql.Pool = await cls._get_read_pool()
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
        pool: aiomysql.Pool = await cls._get_read_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: Dict[str, Any]

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchone()

        return result


class CacheConnection(ABC):
    @classmethod
    @abstractmethod
    async def initialize(cls, connection_info):
        ...

    @classmethod
    @abstractmethod
    async def destroy(cls):
        ...

    @classmethod
    @abstractmethod
    async def set(cls, key: str, value: Dict[str, Any]) -> None:
        ...

    @classmethod
    @abstractmethod
    async def get(cls, key: str) -> Dict[str, Any]:
        ...

    @classmethod
    @abstractmethod
    async def delete(cls, key: str) -> None:
        ...


class RedisConnection(CacheConnection):
    redis: aioredis.Redis = None

    @classmethod
    async def initialize(cls, connection_info):
        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await aioredis.create_redis_pool(**connection_info)

        return cls.redis

    @classmethod
    async def destroy(cls):
        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None

    @classmethod
    async def set(cls, key: str, value: Dict[str, Any]) -> None:
        dumped_value = json.dumps(value)
        await cls.redis.set(key, dumped_value)

    @classmethod
    async def get(cls, key: str) -> Dict[str, Any]:
        value = await cls.redis.get(key)
        value = json.loads(value) if value else None

        return value

    @classmethod
    async def delete(cls, key: str) -> None:
        await cls.redis.delete(key)

    @classmethod
    async def flush_all(cls):
        await cls.redis.flushall()
