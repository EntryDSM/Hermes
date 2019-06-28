import datetime
import random
import uuid
from typing import Type

from tests.helpers.util import (
    DunnoValue,
    generate_random_phone_number,
    generate_random_string,
)
from hermes.entities.applicant import Applicant
from hermes.repositories.applicant import ApplicantPersistentRepository
from hermes.repositories.connections import DBConnection, MySQLConnection


def generate_applicant_id(applicant_index: int):
    return uuid.uuid5(uuid.NAMESPACE_OID, f"applicant:{applicant_index}").hex[0:8]


def generate_applicant_email(applicant_index: int):
    return f"{generate_applicant_id(applicant_index)}@dsm.hs.kr"


async def create_applicant_table(db_connection: Type[DBConnection]):
    await db_connection.execute(ApplicantPersistentRepository.table_creation_query)


def create_applicant_dummy_object(applicant_index: int):
    return Applicant(
        email=generate_applicant_email(applicant_index),
        password=f"pw:{generate_applicant_id(applicant_index)}",
        applicant_name=generate_random_string(),
        sex="FEMALE" if applicant_index % 2 else "MALE",
        birth_date=datetime.datetime.now().date(),
        parent_name=generate_random_string(),
        parent_tel=generate_random_phone_number(),
        applicant_tel=generate_random_phone_number(),
        address=generate_random_string(),
        post_code=random.randint(10000, 99999),
        image_path=generate_random_string(),
    )


async def save_applicants(applicant_dummy_set):
    query = """
        INSERT INTO applicant (
        email,
        password,
        applicant_name, 
        sex, 
        birth_date, 
        parent_name, 
        parent_tel, 
        applicant_tel, 
        address, 
        post_code, 
        image_path
        ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    for applicant in applicant_dummy_set:
        await MySQLConnection.execute(
            query,
            applicant.email,
            applicant.password,
            applicant.applicant_name,
            applicant.sex,
            applicant.birth_date,
            applicant.parent_name,
            applicant.parent_tel,
            applicant.applicant_tel,
            applicant.address,
            applicant.post_code,
            applicant.image_path,
        )


def applicant_response(applicant_index, sex=None):
    return {
        "sex": DunnoValue([str, type(None)]) if not sex else sex,
        "birth_date": DunnoValue([str, type(None)]),
        "address": DunnoValue([str, type(None)]),
        "post_code": DunnoValue([str, type(None)]),
        "parent_tel": DunnoValue([str, type(None)]),
        "email": generate_applicant_email(applicant_index)
        if not sex
        else DunnoValue([str, type(None)]),
        "applicant_tel": DunnoValue([str, type(None)]),
        "applicant_name": DunnoValue([str, type(None)]),
        "image_path": DunnoValue([str, type(None)]),
        "parent_name": DunnoValue([str, type(None)]),
    }


def applicant_batch_response(count, sex=None):
    fake_responses = [applicant_response(i) for i in range(count)]

    if sex:
        fake_responses = [applicant_response(i, sex=sex) for i in range(count)]

    return fake_responses
