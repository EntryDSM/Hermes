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


class UserCache:
    _key_template = "hermes:info:{0}"

    @classmethod
    async def set(cls, user_id, user_info):
        user_info = json.dumps(user_info)
        await Cache.redis.set(cls._key_template.format(user_id), user_info)

    @classmethod
    async def get(cls, user_id):
        user_info = await Cache.redis.get(cls._key_template.format(user_id))
        user_info = json.loads(user_info) if user_info else None

        return user_info

    @classmethod
    async def delete(cls, user_id):
        await Cache.redis.delete(cls._key_template.format(user_id))
