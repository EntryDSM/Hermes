from sanic.log import logger

from hermes.misc.config import settings
from hermes.repositories.connections import MySQLConnection, RedisConnection


async def initialize(app, loop):
    database_connection_info = (
        app.database_connection_info
        if hasattr(app, "database_connection_info")
        else settings.database_connection_info
    )

    cache_connection_info = (
        app.cache_connection_info
        if hasattr(app, "cache_connection_info")
        else settings.cache_connection_info
    )

    await MySQLConnection.initialize(database_connection_info)
    await RedisConnection.initialize(cache_connection_info)
    logger.info("Initialize complete")
    # enable for production


async def release(app, loop):
    await MySQLConnection.destroy()
