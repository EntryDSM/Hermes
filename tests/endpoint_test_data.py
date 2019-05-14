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

