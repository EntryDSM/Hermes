import datetime
import random
from typing import Type

from helpers.applicant import generate_applicant_email
from helpers.util import DunnoValue
from hermes.entities.applicant_status import ApplicantStatus
from hermes.repositories.applicant_status import ApplicantStatusPersistentRepository
from hermes.repositories.connections import DBConnection, MySQLConnection


async def create_applicant_status_table(db_connection: Type[DBConnection]):
    await db_connection.execute(
        ApplicantStatusPersistentRepository.table_creation_query
    )


def create_applicant_status_dummy_object(applicant_index: int):
    return ApplicantStatus(
        applicant_email=generate_applicant_email(applicant_index),
        receipt_code=applicant_index,
        is_paid=random.choice([True, False]),
        is_final_submit=random.choice([True, False]),
        is_passed_first_apply=random.choice([True, False]),
        is_printed_application_arrived=random.choice([True, False]),
        exam_code=random.randint(100000, 999999),
    )


async def save_applicant_statuses(applicant_status_dummy_set):
    query = """
        INSERT INTO applicant_status (
        applicant_email,
        is_final_submit,
        is_passed_first_apply,
        is_paid,
        is_printed_application_arrived,
        exam_code
        ) VALUES (
        %s, %s, %s, %s, %s, %s
        )
    """

    for status in applicant_status_dummy_set:
        await MySQLConnection.execute(
            query,
            status.applicant_email,
            status.is_final_submit,
            status.is_passed_first_apply,
            status.is_paid,
            status.is_printed_application_arrived,
            status.exam_code,
        )


applicant_status_dunno_response = {
    "receipt_code": DunnoValue(int),
    "exam_code": DunnoValue([str, type(None)]),
    "is_printed_application_arrived": DunnoValue(bool),
    "is_final_submit": DunnoValue(bool),
    "is_passed_first_apply": DunnoValue(bool),
    "is_paid": DunnoValue(bool),
}
