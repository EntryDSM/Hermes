# pylint: disable=unused-argument,redefined-outer-name
from dataclasses import asdict

import pytest
from sanic.websocket import WebSocketProtocol

from hermes.presentation.app import create_app
from hermes.repositories.admin import (AdminCacheRepository,
                                       AdminPersistentRepository)
from hermes.repositories.connections import MySQLConnection, RedisConnection
from tests.helpers import (create_admin_dummy_object, create_admin_table,
                           save_admins)


@pytest.fixture(scope="function")
async def mysql_manage(mysql, mysql_proc):
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


@pytest.yield_fixture(scope="function")
async def hermes_app(mysql_proc, mysql, redis_proc):
    _app = create_app()

    _app.database_connection_info = {
        "use_unicode": True,
        "charset": "utf8mb4",
        "user": mysql_proc.user,
        "db": "pytest_mysql_db",
        "host": mysql_proc.host,
        "port": mysql_proc.port,
        "autocommit": True,
    }

    _app.cache_connection_info = {
        "address": f"redis://:@{redis_proc.host}:{redis_proc.port}",
        "minsize": 5,
    }

    yield _app


@pytest.fixture(scope="function")
def test_cli(loop, hermes_app, sanic_client):
    return loop.run_until_complete(sanic_client(hermes_app, protocol=WebSocketProtocol))


