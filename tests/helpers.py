import random
import string
import uuid
from typing import Type

from werkzeug.security import generate_password_hash

from hermes.entities.admin import Admin
from hermes.repositories.connections import DBConnection, MySQLConnection


class DunnoValue:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __eq__(self, other):
        if type(self.expected_type) is list:
            return self._list_eq(other)
        else:
            return self._type_eq(other)

    def _list_eq(self, other):
        for expected_type in self.expected_type:
            if expected_type == uuid.UUID and isinstance(other, str):
                try:
                    uuid.UUID(other)
                except ValueError:
                    return False
                else:
                    return True
            else:
                if isinstance(other, expected_type):
                    return True

        return False

    def _type_eq(self, other):
        if self.expected_type == uuid.UUID and isinstance(other, str):
            try:
                uuid.UUID(other)
            except ValueError:
                return False
            else:
                return True
        else:
            return isinstance(other, self.expected_type)


async def create_admin_table(db_connection: Type[DBConnection]):
    table_creation_query = """
            create table admin
            (
              admin_id       varchar(45)                                  not null
                primary key,
              admin_password varchar(100)                                  not null,
              admin_type     enum ('ROOT', 'ADMINISTRATION', 'INTERVIEW') not null,
              admin_email    varchar(320)                                 not null,
              admin_name     varchar(13)                                  not null,
              created_at     timestamp default CURRENT_TIMESTAMP          not null,
              updated_at     timestamp default CURRENT_TIMESTAMP          not null
            ) character set utf8mb4;
    """
    await db_connection.execute(table_creation_query)


def create_admin_dummy_object(admin_index: int, privileges: str = "ADMINISTRATION"):
    return Admin(
        admin_email=generate_admin_email(admin_index),
        admin_password=generate_random_string(),
        admin_type=privileges,
        admin_id=generate_admin_id(admin_index),
        admin_name=generate_random_string(),
    )


def generate_random_string(length: int = 10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_admin_id(admin_index: int):
    return uuid.uuid5(uuid.NAMESPACE_OID, f"admin: {admin_index}").hex[0:8]


def generate_admin_email(admin_index: int):
    return f"{generate_admin_id(admin_index)}@dsm.hs.kr"


def generate_endpoint_test_data(
    method,
    endpoint,
    query_param,
    request_body,
    expected_response_status,
    expected_response_body,
) -> tuple:
    return (
        method,
        endpoint,
        query_param,
        request_body,
        expected_response_status,
        expected_response_body,
    )


def admin_batch_response(length):
    responses = [
        {
            "admin_id": DunnoValue(str),
            "admin_password": DunnoValue(str),
            "admin_type": DunnoValue(str),
            "admin_email": DunnoValue(str),
            "admin_name": DunnoValue(str),
        }
        for i in range(length)
    ]

    return responses


async def save_admins(admin_dummy_set):
    for admin in admin_dummy_set:
        query = """INSERT INTO admin (
                    admin_id,
                    admin_password,
                    admin_type,
                    admin_email,
                    admin_name
                    ) VALUES (%s, %s, %s, %s, %s)"""

        await MySQLConnection.execute(
            query,
            admin.admin_id,
            generate_password_hash(admin.admin_password),
            admin.admin_type,
            admin.admin_email,
            admin.admin_name,
        )
