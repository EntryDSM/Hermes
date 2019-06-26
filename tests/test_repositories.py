# pylint: disable=unused-argument,redefined-outer-name,invalid-name

from dataclasses import asdict

import pytest

from tests.helpers.admin import generate_admin_id
from tests.helpers.applicant import generate_applicant_email
from hermes.repositories.applicant_status import ApplicantStatusPersistentRepository


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
async def test_applicant_persistent_repo_save(
    mysql_manage, applicant_persistent_repo, applicant_dummy_set
):
    repo = applicant_persistent_repo
    test_data = applicant_dummy_set[0]

    await repo.save(test_data.email, test_data.password)


@pytest.mark.asyncio
async def test_applicant_persistent_repo_patch(
    mysql_manage, applicant_persistent_repo, save_applicant_dummy_to_db
):
    repo = applicant_persistent_repo
    await repo.patch(generate_applicant_email(0), {"password": "p@ssword!"})
    await repo.patch(generate_applicant_email(0), {"applicant_name": "연중모"})
    await repo.patch(generate_applicant_email(0), {"applicant_sex": "MALE"})
    await repo.patch(generate_applicant_email(0), {"post_code": "17002"})


@pytest.mark.asyncio
async def test_applicant_persistent_repo_get(
    mysql_manage, applicant_persistent_repo, save_applicant_dummy_to_db
):
    repo = applicant_persistent_repo
    result = await repo.get_one(generate_applicant_email(0))
    assert generate_applicant_email(0) == result["email"]

    result = await repo.get_list()
    assert isinstance(result, list) and isinstance(result[0], dict)

    result = await repo.get_list({"email": generate_applicant_email(0)})
    assert generate_applicant_email(0) == result[0]["email"]


@pytest.mark.asyncio
async def test_applicant_persistent_repo_delete(
    mysql_manage, applicant_persistent_repo, save_applicant_dummy_to_db
):
    repo = applicant_persistent_repo
    await repo.delete(generate_applicant_email(0))


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


@pytest.mark.asyncio
async def test_applicant_cache_repo_set(
    cache_manage, applicant_cache_repo, applicant_dummy_set
):
    repo = applicant_cache_repo
    test_data = asdict(applicant_dummy_set[0])
    test_data["birth_date"] = str(test_data["birth_date"])

    await repo.set(test_data)


@pytest.mark.asyncio
async def test_applicant_cache_repo_get(
    cache_manage, applicant_cache_repo, save_applicant_dummy_to_cache
):
    repo = applicant_cache_repo
    for i in range(10):
        result = await repo.get(generate_applicant_email(i))
        assert generate_applicant_email(i) == result["email"]


@pytest.mark.asyncio
async def test_applicant_cache_repo_delete(
    cache_manage, applicant_cache_repo, save_applicant_dummy_to_cache
):
    repo = applicant_cache_repo
    for i in range(10):
        await repo.delete(generate_applicant_email(i))


@pytest.mark.asyncio
async def test_applicant_status_persistent_repo_init(
    mysql_manage,
    applicant_status_persistent_repo,
    save_applicant_dummy_to_db,
    applicant_status_dummy_set,
):
    repo: ApplicantStatusPersistentRepository = applicant_status_persistent_repo
    test_data = applicant_status_dummy_set[0]

    await repo.init(test_data.applicant_email)


@pytest.mark.asyncio
async def test_applicant_status_persistent_repo_patch(
    mysql_manage,
    applicant_status_persistent_repo,
    save_applicant_dummy_to_db,
    save_applicant_status_dummy_to_db,
):
    repo: ApplicantStatusPersistentRepository = applicant_status_persistent_repo

    await repo.patch(generate_applicant_email(0), {"is_paid": True})
    await repo.patch(
        generate_applicant_email(0), {"is_printed_application_arrived": False}
    )
    await repo.patch(generate_applicant_email(0), {"exam_code": "029435"})


@pytest.mark.asyncio
async def test_applicant_status_persistent_repo_get(
    mysql_manage,
    applicant_status_persistent_repo,
    save_applicant_dummy_to_db,
    save_applicant_status_dummy_to_db,
):
    repo: ApplicantStatusPersistentRepository = applicant_status_persistent_repo

    for i in range(10):
        result = await repo.get_one(generate_applicant_email(i))
        assert result["applicant_email"] == generate_applicant_email(i)
        assert result["receipt_code"] == i + 1
