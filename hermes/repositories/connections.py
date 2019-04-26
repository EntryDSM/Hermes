from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

import aiomysql
import aioredis
import json


class DBConnection(ABC):
    @classmethod
    @abstractmethod
    async def initialize(cls, connection_info): ...

    @classmethod
    @abstractmethod
    async def destroy(cls): ...

    @classmethod
    @abstractmethod
    async def execute(cls, query: str, *args) -> int: ...

    @classmethod
    @abstractmethod
    async def executemany(cls, query: str, *args) -> int: ...

    @classmethod
    @abstractmethod
    async def fetch(cls, query: str, *args) -> List[Dict[str, Any]]: ...

    @classmethod
    @abstractmethod
    async def fetchone(cls, query: str, *args) -> Dict[str, Any]: ...


class MySQLConnection(DBConnection):
    __read_pool: aiomysql.Pool = None
    __write_pool: aiomysql.Pool = None

    @classmethod
    async def initialize(cls, connection_info):
        await cls._get_read_pool(connection_info)
        await cls._get_write_pool(connection_info)

    @classmethod
    async def destroy(cls):
        if cls.__read_pool is not None:
            cls.__read_pool.close()
            await cls.__read_pool.wait_closed()
        if cls.__write_pool is not None:
            cls.__write_pool.close()
            await cls.__write_pool.wait_closed()

        MySQLConnection.__read_pool = None
        MySQLConnection.__write_pool = None

    @classmethod
    async def _get_read_pool(cls, read_connection_info=None) -> aiomysql.Pool:
        if cls.__read_pool and not cls.__read_pool._closed:
            return cls.__read_pool

        cls.__read_pool = await aiomysql.create_pool(**read_connection_info)

        return cls.__read_pool

    @classmethod
    async def _get_write_pool(cls, write_connection_info=None) -> aiomysql.Pool:
        if cls.__write_pool and not cls.__write_pool._closed:
            return cls.__write_pool

        cls.__write_pool = await aiomysql.create_pool(**write_connection_info)

        return cls.__write_pool

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
    async def initialize(cls, connection_info): ...

    @classmethod
    @abstractmethod
    async def destroy(cls): ...

    @classmethod
    @abstractmethod
    async def set(cls, key: str, value: Dict[str, Any]) -> None: ...

    @classmethod
    @abstractmethod
    async def get(cls, key: str) -> Dict[str, Any]: ...

    @classmethod
    @abstractmethod
    async def delete(cls, key: str) -> None: ...


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
        value = json.dumps(value)
        await cls.redis.set(key, value)

    @classmethod
    async def get(cls, key: str) -> Optional[Dict[str, Any]]:
        value = await cls.redis.get(key)
        value = json.loads(value) if value else None

        return value

    @classmethod
    async def delete(cls, key: str) -> None:
        await cls.redis.delete(key)

    @classmethod
    async def flush_all(cls):
        await cls.redis.flushall()
