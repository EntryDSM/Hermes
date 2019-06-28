import uuid
from typing import Type

from werkzeug.security import generate_password_hash

from tests.helpers.util import DunnoValue, generate_random_string
from hermes.entities.admin import Admin
from hermes.repositories.connections import DBConnection, MySQLConnection


def generate_admin_id(admin_index: int):
    return uuid.uuid5(uuid.NAMESPACE_OID, f"admin: {admin_index}").hex[0:8]


def generate_admin_email(admin_index: int):
    return f"{generate_admin_id(admin_index)}@dsm.hs.kr"


async def create_admin_table(
    db_connection: Type[DBConnection]
):  # TODO: must get query from repo!!
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
        admin_password=f"pw:{generate_admin_id(admin_index)}",
        admin_type=privileges,
        admin_id=generate_admin_id(admin_index),
        admin_name=generate_random_string(),
    )


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


def admin_batch_response(length):
    responses = [
        {
            "admin_id": DunnoValue(str),
            "admin_type": DunnoValue(str),
            "admin_email": DunnoValue(str),
            "admin_name": DunnoValue(str),
        }
        for i in range(length)
    ]

    return responses


def admin_detail_response(index):
    return {
        "admin_id": generate_admin_id(index),
        "admin_type": DunnoValue(str),
        "admin_email": generate_admin_email(index),
        "admin_name": DunnoValue(str),
    }
