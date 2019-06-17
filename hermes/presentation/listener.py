from sanic.log import logger

from hermes.misc.config import settings
from hermes.repositories.connections import MySQLConnection, RedisConnection
from hermes.repositories.admin import AdminPersistentRepository
from hermes.repositories.applicant import ApplicantPersistentRepository
from hermes.repositories.applicant_status import ApplicantStatusPersistentRepository


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

    logger.info("Connection initialize complete")


async def migrate(app, loop):
    if not MySQLConnection.is_available:
        raise Exception(
            "Database connection is unavailable, Make sure you initialize connection!"
        )

    await MySQLConnection.execute(AdminPersistentRepository.table_creation_query)
    await MySQLConnection.execute(ApplicantPersistentRepository.table_creation_query)
    await MySQLConnection.execute(ApplicantStatusPersistentRepository.table_creation_query)

    logger.info("Database migration complete")


async def release(app, loop):
    await MySQLConnection.destroy()
    await RedisConnection.destroy()

    # All connections must be destroyed before teardown!
