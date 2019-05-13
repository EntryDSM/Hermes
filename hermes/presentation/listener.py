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

async def migrate(app, loop):
    if not MySQLConnection.is_available:
        raise Exception("Database connection is unavailable, Make sure initialize connection!")

    await MySQLConnection.execute("""
            create table if not exists admin
            (
              admin_id       varchar(45)                                  not null
                primary key,
              admin_password varchar(100)                                 not null,
              admin_type     enum ('ROOT', 'ADMINISTRATION', 'INTERVIEW') not null,
              admin_email    varchar(320)                                 not null,
              admin_name     varchar(13)                                  not null,
              created_at     timestamp default CURRENT_TIMESTAMP          not null,
              updated_at     timestamp default CURRENT_TIMESTAMP          not null
            ) character set utf8mb4;
    """)

    logger.info("Database migration complete")


async def release(app, loop):
    await MySQLConnection.destroy()
