import datetime

from tests.helpers.admin import (
    admin_batch_response,
    admin_detail_response,
    generate_admin_email,
    generate_admin_id,
)
from tests.helpers.applicant import (
    applicant_batch_response,
    applicant_response,
    generate_applicant_email,
    generate_applicant_id)
from tests.helpers.applicant_status import applicant_status_dunno_response
from tests.helpers.util import (
    generate_endpoint_test_data,
    generate_random_string,
    status_message_response,
)


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
            method="GET",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=admin_detail_response(0),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint=f"/api/v1/admin/fakeAdminId",
            query_param={},
            request_body={},
            expected_response_status=404,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={"admin_type": "INTERVIEW"},
            expected_response_status=200,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={"admin_asdf": "something"},
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/admin/xxx",
            query_param={},
            request_body={"admin_type": "INTERVIEW"},
            expected_response_status=404,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="DELETE",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="DELETE",
            endpoint=f"/api/v1/admin/xxx",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def admin_authorization_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="POST",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}/authorization",
            query_param={},
            request_body={
                "password": f"pw:{generate_admin_id(0)}",
            },
            expected_response_status=200,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}/authorization",
            query_param={},
            request_body={
                "password": f"WrongPassWord",
            },
            expected_response_status=403,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint=f"/api/v1/admin/{generate_admin_id(0)}/authorization",
            query_param={},
            request_body={},
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def applicant_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="POST",
            endpoint="/api/v1/applicant",
            query_param={},
            request_body={
                "email": generate_applicant_email(11),
                "password": generate_random_string(),
            },
            expected_response_status=201,
            expected_response_body={
                **applicant_response(11),
                "status": applicant_status_dunno_response,
            },
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint="/api/v1/applicant",
            query_param={},
            request_body={
                "email": generate_applicant_email(0),
                "password": generate_random_string(),
            },
            expected_response_status=409,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint="/api/v1/applicant",
            query_param={},
            request_body={
                "email": generate_applicant_email(11),
                "pssword": generate_random_string(),
            },
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def applicant_batch_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/applicant/batch",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=applicant_batch_response(10),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/applicant/batch",
            query_param={"email": generate_applicant_email(0)},
            request_body={},
            expected_response_status=200,
            expected_response_body=applicant_batch_response(1),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/applicant/batch",
            query_param={"sex": "FEMALE"},
            request_body={},
            expected_response_status=200,
            expected_response_body=applicant_batch_response(5, sex="FEMALE"),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint="/api/v1/applicant/batch",
            query_param={"email": generate_applicant_email(14)},
            request_body={},
            expected_response_status=200,
            expected_response_body=applicant_batch_response(0),
        ),
    ]

    return test_set


def applicant_detail_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="GET",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(0)}",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=applicant_response(0),
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(19)}",
            query_param={},
            request_body={},
            expected_response_status=404,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(3)}",
            query_param={},
            request_body={"password": "ch@nged_p@sswo!rd"},
            expected_response_status=200,
            expected_response_body=applicant_response(3),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(4)}",
            query_param={},
            request_body={"address": "Seattle, WA"},
            expected_response_status=200,
            expected_response_body=applicant_response(4),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(5)}",
            query_param={},
            request_body={"birth_date": str(datetime.datetime.now().date())},
            expected_response_status=200,
            expected_response_body=applicant_response(5),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(6)}",
            query_param={},
            request_body={
                "birth_date": str(datetime.datetime.now().date()),
                "my_name": "post malone",
            },
            expected_response_status=200,
            expected_response_body=applicant_response(6),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(7)}",
            query_param={},
            request_body={"my_favorite_food": "sushi"},
            expected_response_status=200,
            expected_response_body=applicant_response(7),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(6)}",
            query_param={},
            request_body={
                "birth_date": "WrongDateTypeLMAO",
            },
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def applicant_authorization_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="POST",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(0)}/authorization",
            query_param={},
            request_body={
                "password": f"pw:{generate_applicant_id(0)}",
            },
            expected_response_status=200,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(0)}/authorization",
            query_param={},
            request_body={
                "password": f"WrongPassWord",
            },
            expected_response_status=403,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="POST",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(0)}/authorization",
            query_param={},
            request_body={},
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set


def applicant_status_view_test_data():
    test_set = [
        generate_endpoint_test_data(
            method="GET",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(0)}/status",
            query_param={},
            request_body={},
            expected_response_status=200,
            expected_response_body=applicant_status_dunno_response,
        ),
        generate_endpoint_test_data(
            method="GET",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(14)}/status",
            query_param={},
            request_body={},
            expected_response_status=404,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(2)}/status",
            query_param={},
            request_body={"exam_code": "035633"},
            expected_response_status=200,
            expected_response_body=applicant_status_dunno_response,
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(3)}/status",
            query_param={},
            request_body={"is_prd_application_arrived": "true"},
            expected_response_status=200,
            expected_response_body=applicant_status_dunno_response,
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(13)}/status",
            query_param={},
            request_body={"is_printed_application_arrived": "true"},
            expected_response_status=404,
            expected_response_body=status_message_response(),
        ),
        generate_endpoint_test_data(
            method="PATCH",
            endpoint=f"/api/v1/applicant/{generate_applicant_email(4)}/status",
            query_param={},
            request_body={"is_printed_application_arrived": "ThisISNotBooleanType"},
            expected_response_status=400,
            expected_response_body=status_message_response(),
        ),
    ]

    return test_set
