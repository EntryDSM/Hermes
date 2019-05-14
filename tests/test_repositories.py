from dataclasses import asdict

import pytest

from tests.helpers import generate_admin_id


@pytest.mark.asyncio
async def test_admin_persistent_repo_save(
    mysql_manage, admin_persistent_repo, admin_dummy_set
):
    repo = admin_persistent_repo
    test_data = asdict(admin_dummy_set[0])

    await repo.save(test_data)


@pytest.mark.asyncio
async def test_admin_persistent_repo_patch(
    mysql_manage, admin_persistent_repo, save_admin_dummy_to_db
):
    repo = admin_persistent_repo

    await repo.patch(generate_admin_id(0), {"admin_type": "INTERVIEW"})


@pytest.mark.asyncio
async def test_admin_persistent_repo_get(
    mysql_manage, admin_persistent_repo, save_admin_dummy_to_db
):
    repo = admin_persistent_repo

    result = await repo.get_one(generate_admin_id(0))
    assert generate_admin_id(0) == result["admin_id"]

    result = await repo.get_list()
    assert isinstance(result, list) and isinstance(result[0], dict)

    result = await repo.get_list({"admin_type": "ROOT"})
    assert isinstance(result, list) and generate_admin_id(0) == result[0]["admin_id"]


@pytest.mark.asyncio
async def test_admin_persistent_repo_delete(
    mysql_manage, admin_persistent_repo, save_admin_dummy_to_db
):
    repo = admin_persistent_repo

    await repo.delete(generate_admin_id(0))


@pytest.mark.asyncio
async def test_admin_cache_repo_set(cache_manage, admin_cache_repo, admin_dummy_set):
    repo = admin_cache_repo
    test_data = asdict(admin_dummy_set[0])

    await repo.set(test_data)


@pytest.mark.asyncio
async def test_admin_cache_repo_get(
    cache_manage, admin_cache_repo, save_admin_dummy_to_cache
):
    repo = admin_cache_repo

    for i in range(0, 10):
        result = await repo.get(generate_admin_id(i))
        assert generate_admin_id(i) == result["admin_id"]


@pytest.mark.asyncio
async def test_admin_cache_repo_delete(
    cache_manage, admin_cache_repo, save_admin_dummy_to_cache
):
    repo = admin_cache_repo

    for i in range(0, 10):
        await repo.delete(generate_admin_id(i))
