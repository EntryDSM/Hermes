# pylint: disable=unused-argument,redefined-outer-name
import pytest

from hermes.presentation.app import create_app
from hermes.repositories.connections import MySQLConnection, RedisConnection


@pytest.fixture(scope="function")
async def mysql_manage(mysql_proc):
    conn_info = {
        "use_unicode": True,
        "charset": "utf8mb4",
        "user": mysql_proc.user,
        "db": "pytest_mysql_db",
        "host": mysql_proc.host,
        "port": mysql_proc.port,
        "loop": None,
        "autocommit": True,
    }
    await MySQLConnection.initialize(conn_info)
    yield
    await MySQLConnection.destroy()


@pytest.fixture(scope="function")
async def cache_manage(redis_proc):
    conn_info = {
        "address": f"redis://:@{redis_proc.host}:{redis_proc.port}",
        "minsize": 5,
        "maxsize": 10,
    }
    await RedisConnection.initialize(conn_info)
    await RedisConnection.flush_all()
    yield
    await RedisConnection.destroy()


@pytest.fixture(scope="function")
async def hermes_app(mysql_proc, mysql, redis_proc):
    _app = create_app()

    _app.database_connection_info = {
        "use_unicode": True,
        "charset": "utf8mb4",
        "user": mysql_proc.user,
        "db": "pytest_mysql_db",
        "host": mysql_proc.host,
        "port": mysql_proc.port,
        "loop": None,
        "autocommit": True,
    }

    _app.cache_connection_info = {
        "address": f"redis://:@{redis_proc.host}:{redis_proc.port}",
        "minsize": 5,
        "maxsize": 10,
    }

    return _app.test_client

