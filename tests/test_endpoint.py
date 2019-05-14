import json

import pytest

from helpers import save_admins
from tests.endpoint_test_data import (
    admin_batch_view_test_data,
    admin_view_test_data,
    admin_detail_view_test_data,
)


@pytest.mark.parametrize(
    "method,endpoint,query_param,request_body,expected_response_status,expected_response_body",
    admin_view_test_data()
    + admin_batch_view_test_data()
    + admin_detail_view_test_data(),
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
):
    await save_admins(admin_dummy_set)

    r = await getattr(test_cli, method.lower())(
        uri=endpoint, params=query_param, data=json.dumps(request_body)
    )

    assert r.status == expected_response_status
    assert await r.json() == expected_response_body
