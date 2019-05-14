import pytest
from aioredis.errors import RedisError
from pymysql.err import MySQLError

from hermes.repositories.connections import MySQLConnection, RedisConnection


@pytest.mark.asyncio
@pytest.mark.parametrize("db_method", ["execute", "executemany", "fetch", "fetchone"])
async def test_db_connection_interface(db_method, mysql_manage):
    try:
        await getattr(MySQLConnection, db_method)("SELECT 1")
    except MySQLError as e:
        assert (
            False
        ), f"expected success, but error: '{e}' occurred while testing method '{db_method}'."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cache_method, param",
    [
        ("set", {"key": "x", "value": {"y": 0}}),
        ("get", {"key": "x"}),
        ("delete", {"key": "x"}),
        ("flush_all", {}),
    ],
)
async def test_cache_connection_interface(cache_method, param, cache_manage):
    try:
        await getattr(RedisConnection, cache_method)(**param)
    except RedisError as e:
        assert (
            False
        ), f"expected success, but error: '{e}' occurred while testing method '{cache_method}'."
