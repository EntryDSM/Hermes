import aioredis
import json

from hermes.config import settings


class Cache:
    redis: aioredis.Redis = None

    @classmethod
    async def initialize(cls):
        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await aioredis.create_redis_pool(
            f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}',
            minsize=5, maxsize=10)

        return cls.redis

    @classmethod
    async def destroy(cls):
        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None

    @classmethod
    async def set(cls, directory, key, value, expire=None):
        await cls.redis.set(f"user:{directory}:{key}", value, expire=expire)

    @classmethod
    async def get(cls, directory, key):
        return await cls.redis.get(f"user:{directory}:{key}")

    @classmethod
    async def delete(cls, directory, key):
        await cls.redis.delete(f"user:{directory}:{key}")


class UserCache:
    @staticmethod
    async def set(user_id, user_info):
        user_info = json.dumps(user_info)
        await Cache.set("info", user_id, user_info)

    @staticmethod
    async def get(user_id):
        user_info = await Cache.get("info", user_id)
        user_info = json.loads(user_info) if user_info else None

        return user_info

    @staticmethod
    async def delete(user_id):
        await Cache.delete("info", user_id)
