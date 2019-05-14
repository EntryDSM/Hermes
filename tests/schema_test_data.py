import datetime
import random
from typing import Any, Dict, Union, Tuple, List, Type

from marshmallow import Schema

from hermes.adapters.schema import (AdminSchema, ApplicantSchema,
                                    ApplicantStatusSchema)

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

