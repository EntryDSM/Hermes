from tests.helpers import (
    admin_batch_response,
    generate_admin_email,
    generate_admin_id,
    generate_endpoint_test_data,
    generate_random_string,
    status_message_response,
    admin_detail_response)


def admin_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="POST",
            endpoint="/api/v1/admin",
            query_param={},
            request_body={
                "admin_id": generate_admin_id(11),
                "admin_email": generate_admin_email(11),
                "admin_name": generate_random_string(),
                "admin_password": generate_random_string(),
                "admin_type": "ROOT",
            },
            expected_response_status=201,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint="/api/v1/admin",
            query_param={},
            request_body={
                "admin_id": generate_admin_id(11),
                "admin_name": generate_random_string(),
                "admin_password": generate_random_string(),
                "admin_type": "ROOT",
            },
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint="/api/v1/admin",
            query_param={},
            request_body={
                "admin_id": generate_admin_id(0),
                "admin_email": generate_admin_email(0),
                "admin_name": generate_random_string(),
                "admin_password": generate_random_string(),
                "admin_type": "ROOT",
            },
            expected_response_status=409,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def admin_batch_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/admin/batch",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=admin_batch_response(10),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/admin/batch",
            query_param={"admin_id": generate_admin_id(0)},
            request_body={},
            expected_response_status=200,
            expected_response_body=admin_batch_response(1),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/admin/batch",
            query_param={"admin_type": "INTERVIEW"},
            request_body={},
            expected_response_status=200,
            expected_response_body=admin_batch_response(5),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/admin/batch",
            query_param={"admin_email": generate_admin_email(0)},
            request_body={},
            expected_response_status=200,
            expected_response_body=admin_batch_response(1),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/admin/batch",
            query_param={"admin_eml": "asdf"},
            request_body={},
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def admin_detail_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method='GET',
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=admin_detail_response(0)
        ),
        generate_endpoint_test_data(
            method='GET',
            endpoint=f"/api/v1/admin/fakeAdminId",
            query_param={},
            request_body={},
            expected_response_status=404,
            expected_response_body=status_message_response()
        ),
        generate_endpoint_test_data(
            method='PATCH',
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={
                "admin_type": "INTERVIEW"
            },
            expected_response_status=200,
            expected_response_body=status_message_response()
        ),
        generate_endpoint_test_data(
            method='PATCH',
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={
                "admin_asdf": "something"
            },
            expected_response_status=400,
            expected_response_body=status_message_response()
        ),
        generate_endpoint_test_data(
            method='PATCH',
            endpoint=f"/api/v1/admin/xxx",
            query_param={},
            request_body={
                "admin_type": "INTERVIEW"
            },
            expected_response_status=404,
            expected_response_body=status_message_response()
        ),
        generate_endpoint_test_data(
            method='DELETE',
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=status_message_response()
        ),
        generate_endpoint_test_data(
            method='DELETE',
            endpoint=f"/api/v1/admin/xxx",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=status_message_response()
        )
    ]

    return test_set
