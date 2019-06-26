# pylint: disable=unused-argument,redefined-outer-name
from dataclasses import asdict

import pytest
from sanic.websocket import WebSocketProtocol

from hermes.presentation.app import create_app
from hermes.repositories.admin import AdminCacheRepository, AdminPersistentRepository
from hermes.repositories.applicant import (
    ApplicantCacheRepository,
    ApplicantPersistentRepository,
)
from hermes.repositories.applicant_status import (
    ApplicantStatusCacheRepository,
    ApplicantStatusPersistentRepository,
)
from hermes.repositories.connections import MySQLConnection, RedisConnection
from tests.helpers.admin import (
    create_admin_dummy_object,
    create_admin_table,
    save_admins,
)
from tests.helpers.applicant import (
    create_applicant_dummy_object,
    create_applicant_table,
    save_applicants,
)
from tests.helpers.applicant_status import (
    create_applicant_status_dummy_object,
    create_applicant_status_table,
    save_applicant_statuses,
)


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
    await create_admin_table(MySQLConnection)
    await create_applicant_table(MySQLConnection)
    await create_applicant_status_table(MySQLConnection)
    yield
    await MySQLConnection.destroy()


@pytest.fixture(scope="function")
async def cache_manage(redisdb, redis_proc):
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
async def hermes_app(mysql_proc, mysql, redis_proc, redisdb):
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


@pytest.fixture(scope="function")
def admin_dummy_set():
    admins = (
        [create_admin_dummy_object(0, "ROOT")]
        + [create_admin_dummy_object(i, "ADMINISTRATION") for i in range(1, 5)]
        + [create_admin_dummy_object(i, "INTERVIEW") for i in range(5, 10)]
    )

    return admins


@pytest.fixture(scope="function")
def applicant_dummy_set():
    applicants = [create_applicant_dummy_object(i) for i in range(10)]
    return applicants


@pytest.fixture(scope="function")
def applicant_status_dummy_set():
    statuses = [create_applicant_status_dummy_object(i) for i in range(10)]
    return statuses


@pytest.fixture(scope="function")
async def save_admin_dummy_to_db(admin_dummy_set):

    await save_admins(admin_dummy_set)


@pytest.fixture(scope="function")
async def save_applicant_dummy_to_db(applicant_dummy_set):

    await save_applicants(applicant_dummy_set)


@pytest.fixture(scope="function")
async def save_applicant_status_dummy_to_db(
    save_applicant_dummy_to_db, applicant_status_dummy_set
):

    await save_applicant_statuses(applicant_status_dummy_set)


@pytest.fixture(scope="function")
async def save_admin_dummy_to_cache(admin_dummy_set):
    for admin in admin_dummy_set:
        await RedisConnection.set(f"hermes:admin:{admin.admin_id}", asdict(admin))

    return


@pytest.fixture(scope="function")
async def save_applicant_dummy_to_cache(applicant_dummy_set):
    for applicant in applicant_dummy_set:
        applicant = asdict(applicant)
        applicant["birth_date"] = str(applicant["birth_date"])

        await RedisConnection.set(
            ApplicantCacheRepository._key_template.format(applicant["email"]), applicant
        )


@pytest.fixture(scope="function")
async def save_applicant_status_dummy_to_cache(applicant_status_dummy_set):
    for status in applicant_status_dummy_set:
        await RedisConnection.set(
            ApplicantStatusCacheRepository._key_template.format(status.applicant_email),
            asdict(status),
        )


@pytest.fixture(scope="function")
async def admin_persistent_repo():
    repo = AdminPersistentRepository(MySQLConnection)

    return repo


@pytest.fixture(scope="function")
async def applicant_persistent_repo():
    repo = ApplicantPersistentRepository(MySQLConnection)

    return repo


@pytest.fixture(scope="function")
async def applicant_status_persistent_repo():
    repo = ApplicantStatusPersistentRepository(MySQLConnection)

    return repo


@pytest.fixture(scope="function")
async def admin_cache_repo():
    repo = AdminCacheRepository(RedisConnection)

    return repo


@pytest.fixture(scope="function")
async def applicant_cache_repo():
    repo = ApplicantCacheRepository(RedisConnection)

    return repo


@pytest.fixture(scope="function")
async def applicant_status_cache_repo():
    repo = ApplicantStatusCacheRepository(RedisConnection)

    return repo
