# pylint: disable=unused-argument,redefined-outer-name

import datetime
import random
from typing import Any, Dict, Union, Tuple, List, Type

from marshmallow import Schema

from hermes.adapters.schema import AdminSchema, ApplicantSchema, ApplicantStatusSchema

EXPECTED_SUCCESS = True
EXPECTED_FAIL = False


class SchemaTestData:
    schema: Type[Schema]
    schema_test_set: List[Tuple[Union[Dict[Any, Any], bool]]]

    @classmethod
    def get_test_data(cls):
        return [(cls.schema, *test_set) for test_set in cls.schema_test_set]


class AdminSchemaTestData(SchemaTestData):
    schema = AdminSchema

    VALID_ADMIN_ID = "admin_id"
    VALID_ADMIN_TYPE = ["ROOT", "ADMIN", "INTERVIEW"]
    VALID_ADMIN_EMAIL = "admin@dsm.hs.kr"
    VALID_ADMIN_NAME = "홍길동"
    VALID_ADMIN_PW = "p@ssword"

    INVALID_ADMIN_ID = "X" * 46
    INVALID_ADMIN_TYPE = ["RO0T", "AADMIN", "lNTERVIEW"]
    INVALID_ADMIN_EMAIL = "admin@somewhere"
    INVALID_ADMIN_NAME = "가" * 14
    INVALID_ADMIN_PW = "P" * 14

    schema_test_set = [
        (
            {
                "admin_id": VALID_ADMIN_ID,
                "admin_type": VALID_ADMIN_TYPE[random.randint(0, 2)],
                "admin_email": VALID_ADMIN_EMAIL,
                "admin_name": VALID_ADMIN_NAME,
                "admin_password": VALID_ADMIN_PW,
            },
            EXPECTED_SUCCESS,
        ),
        # admin_id validation failure case
        (
            {
                "admin_id": INVALID_ADMIN_ID,
                "admin_type": VALID_ADMIN_TYPE[random.randint(0, 2)],
                "admin_email": VALID_ADMIN_EMAIL,
                "admin_name": VALID_ADMIN_NAME,
                "admin_password": VALID_ADMIN_PW,
            },
            EXPECTED_FAIL,
        ),
        # admin_type validation failure case
        (
            {
                "admin_id": VALID_ADMIN_ID,
                "admin_type": INVALID_ADMIN_TYPE[random.randint(0, 2)],
                "admin_email": VALID_ADMIN_EMAIL,
                "admin_name": VALID_ADMIN_NAME,
                "admin_password": VALID_ADMIN_PW,
            },
            EXPECTED_FAIL,
        ),
        # admin_email validation failure case
        (
            {
                "admin_id": VALID_ADMIN_ID,
                "admin_type": VALID_ADMIN_TYPE[random.randint(0, 2)],
                "admin_email": INVALID_ADMIN_EMAIL,
                "admin_name": VALID_ADMIN_NAME,
                "admin_password": VALID_ADMIN_PW,
            },
            EXPECTED_FAIL,
        ),
        # admin_name validation failure case
        (
            {
                "admin_id": VALID_ADMIN_ID,
                "admin_type": VALID_ADMIN_TYPE[random.randint(0, 2)],
                "admin_email": VALID_ADMIN_EMAIL,
                "admin_name": INVALID_ADMIN_NAME,
                "admin_password": VALID_ADMIN_PW,
            },
            EXPECTED_FAIL,
        ),
        # admin_password validation failure case
        (
            {
                "admin_id": VALID_ADMIN_ID,
                "admin_type": VALID_ADMIN_TYPE[random.randint(0, 2)],
                "admin_email": VALID_ADMIN_EMAIL,
                "admin_name": VALID_ADMIN_NAME,
                "admin_password": INVALID_ADMIN_PW,
            },
            EXPECTED_FAIL,
        ),
    ]


class ApplicantSchemaTestData(SchemaTestData):
    schema = ApplicantSchema

    VALID_EMAIL = "applicant@dsm.hs.kr"
    VALID_PW = "p@ssword"
    VALID_APPLICANT_NAME = "홍길동"
    VALID_SEX = ["MALE", "FEMALE"]
    VALID_BIRTH_DATE = str(datetime.datetime.now().date())
    VALID_PARENT_NAME = "홍판서"
    VALID_PARENT_TEL = "010-1234-5678"
    VALID_APPLICANT_TEL = "010-2345-3456"
    VALID_ADDRESS = "서울시 강남구 봉은사로 22"
    VALID_POST_CODE = "12312"
    VALID_IMAGE_PATH = "/path/to/store/this.img"

    INVALID_EMAIL = "applicant@somewhere"
    INVALID_PW = "P" * 333
    INVALID_APPLICANT_NAME = "홍" * 14
    INVALID_SEX = ["MaLE", "FEEEMALE"]
    INVALID_BIRTH_DATE = object
    INVALID_PARENT_NAME = "판" * 13
    INVALID_PARENT_TEL = "10-1235678"
    INVALID_APPLICANT_TEL = "0345-3456"
    INVALID_ADDRESS = "주" * 501
    INVALID_POST_CODE = "1" * 6
    INVALID_IMAGE_PATH = "PATH" * 65

    schema_test_set = [
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW[0],
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_SUCCESS,
        ),
        # email validation failure case
        (
            {
                "email": INVALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # password validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": INVALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # applicant_name validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": INVALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # sex validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": INVALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # birth_date validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": INVALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # parent_name validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": INVALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # parent_tel validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": INVALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # applicant_tel validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": INVALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # address validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": INVALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # post_code validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": INVALID_POST_CODE,
                "image_path": VALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
        # image_path validation failure case
        (
            {
                "email": VALID_EMAIL,
                "password": VALID_PW,
                "applicant_name": VALID_APPLICANT_NAME,
                "sex": VALID_SEX[random.randint(0, 1)],
                "birth_date": VALID_BIRTH_DATE,
                "parent_name": VALID_PARENT_NAME,
                "parent_tel": VALID_PARENT_TEL,
                "applicant_tel": VALID_APPLICANT_TEL,
                "address": VALID_ADDRESS,
                "post_code": VALID_POST_CODE,
                "image_path": INVALID_IMAGE_PATH,
            },
            EXPECTED_FAIL,
        ),
    ]


class ApplicantStatusSchemaTestData(SchemaTestData):
    schema = ApplicantStatusSchema

    VALID_APPLICANT_EMAIL = "applicant@dsm.hs.kr"
    VALID_RECEIPT_CODE = 1
    VALID_IS_PAID = [True, False]
    VALID_IS_PRINTED_APPLICATION_ARRIVED = [True, False]  # pylint: disable=invalid-name
    VALID_IS_PASSED_FIRST_APPLY = [True, False]
    VALID_IS_FINAL_SUBMIT = [True, False]
    VALID_EXAM_CODE = "100001"

    INVALID_APPLICANT_EMAIL = "applicant@dsm.hs.kr"
    INVALID_RECEIPT_CODE = "A"
    INVALID_IS_PAID = ["TrUe", "faLsE"]
    INVALID_IS_PRINTED_APPLICATION_ARRIVED = [  # pylint: disable=invalid-name
        "TrUe",
        "faLsE",
    ]
    INVALID_IS_PASSED_FIRST_APPLY = ["TrUe", "faLsE"]  # pylint: disable=invalid-name
    INVALID_IS_FINAL_SUBMIT = ["TrUe", "faLsE"]
    INVALID_EXAM_CODE = True

    schema_test_set = [
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": VALID_RECEIPT_CODE,
                "is_paid": random.choice(VALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    VALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(VALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(VALID_IS_FINAL_SUBMIT),
                "exam_code": VALID_EXAM_CODE,
            },
            EXPECTED_SUCCESS,
        ),
        # receipt_code validation failure case
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": INVALID_RECEIPT_CODE,
                "is_paid": random.choice(VALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    VALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(VALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(VALID_IS_FINAL_SUBMIT),
                "exam_code": VALID_EXAM_CODE,
            },
            EXPECTED_FAIL,
        ),
        # is_paid validation failure case
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": VALID_RECEIPT_CODE,
                "is_paid": random.choice(INVALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    VALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(VALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(VALID_IS_FINAL_SUBMIT),
                "exam_code": VALID_EXAM_CODE,
            },
            EXPECTED_FAIL,
        ),
        # is_printed... validation failure case
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": VALID_RECEIPT_CODE,
                "is_paid": random.choice(VALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    INVALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(VALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(VALID_IS_FINAL_SUBMIT),
                "exam_code": VALID_EXAM_CODE,
            },
            EXPECTED_FAIL,
        ),
        # is_passed... validation failure case
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": VALID_RECEIPT_CODE,
                "is_paid": random.choice(VALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    VALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(INVALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(VALID_IS_FINAL_SUBMIT),
                "exam_code": VALID_EXAM_CODE,
            },
            EXPECTED_FAIL,
        ),
        # is_final_submit validation failure case
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": VALID_RECEIPT_CODE,
                "is_paid": random.choice(VALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    VALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(VALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(INVALID_IS_FINAL_SUBMIT),
                "exam_code": VALID_EXAM_CODE,
            },
            EXPECTED_FAIL,
        ),
        # exam_code validation failure case
        (
            {
                "applicant_email": VALID_APPLICANT_EMAIL,
                "receipt_code": VALID_RECEIPT_CODE,
                "is_paid": random.choice(VALID_IS_PAID),
                "is_printed_application_arrived": random.choice(
                    VALID_IS_PRINTED_APPLICATION_ARRIVED
                ),
                "is_passed_first_apply": random.choice(VALID_IS_PASSED_FIRST_APPLY),
                "is_final_submit": random.choice(VALID_IS_FINAL_SUBMIT),
                "exam_code": INVALID_EXAM_CODE,
            },
            EXPECTED_FAIL,
        ),
    ]
