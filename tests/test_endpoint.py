# pylint: disable=unused-argument,redefined-outer-name,too-many-arguments

import json

import pytest

from tests.helpers.admin import save_admins
from tests.helpers.applicant import save_applicants
from tests.helpers.applicant_status import save_applicant_statuses
from tests.endpoint_test_data import (
    admin_batch_view_test_data,
    admin_detail_view_test_data,
    admin_view_test_data,
    applicant_batch_view_test_data,
    applicant_detail_view_test_data,
    applicant_status_view_test_data,
    applicant_view_test_data,
    applicant_authorization_view_test_data,
)


@pytest.mark.parametrize(
    "method,endpoint,query_param,request_body,expected_response_status,expected_response_body",
    admin_view_test_data()
    + admin_batch_view_test_data()
    + admin_detail_view_test_data()
    + applicant_view_test_data()
    + applicant_batch_view_test_data()
    + applicant_detail_view_test_data()
    + applicant_authorization_view_test_data()
    + applicant_status_view_test_data(),
)
async def test_endpoint(
    test_cli,
    method,
    endpoint,
    query_param,
    request_body,
    expected_response_status,
    expected_response_body,
    admin_dummy_set,
    applicant_dummy_set,
    applicant_status_dummy_set,
):
    await save_admins(admin_dummy_set)
    await save_applicants(applicant_dummy_set)
    await save_applicant_statuses(applicant_status_dummy_set)

    r = await getattr(test_cli, method.lower())(
        uri=endpoint, params=query_param, data=json.dumps(request_body)
    )

    assert r.status == expected_response_status

    actual_body = await r.json()

    if isinstance(actual_body, list):
        for expected in expected_response_body:
            if expected not in actual_body:
                assert False
    else:
        assert actual_body == expected_response_body
