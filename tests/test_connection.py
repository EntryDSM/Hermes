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

