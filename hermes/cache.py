from typing import Union, Dict

import aioredis
import json

from hermes.config import settings


class Cache:
    redis: aioredis.Redis = None

    @classmethod
    async def initialize(cls) -> aioredis.Redis:
        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await aioredis.create_redis_pool(
            f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}',
            minsize=5, maxsize=10)

        return cls.redis

    @classmethod
    async def destroy(cls) -> None:
        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None


class UserCache:
    _key_template: str = "hermes:info:{0}"

    @classmethod
    async def set(cls, user_id: str, user_info: dict) -> None:
        user_info = json.dumps(user_info)
        await Cache.redis.set(cls._key_template.format(user_id), user_info)

    @classmethod
    async def get(cls, user_id: str) -> Union[Dict, None]:
        user_info = await Cache.redis.get(cls._key_template.format(user_id))
        user_info = json.loads(user_info) if user_info else None

        return user_info

    @classmethod
    async def delete(cls, user_id) -> None:
        await Cache.redis.delete(cls._key_template.format(user_id))
