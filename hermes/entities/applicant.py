from dataclasses import dataclass
from datetime import date


@dataclass
class Applicant:
    email: str
    password: str
    applicant_name: str
    sex: str
    birth_date: date
    parent_name: str
    parent_tel: str
    applicant_tel: str
    address: str
    post_code: str
    image_path: str


@dataclass
class ApplicantStatus:
    applicant_email: str
    receipt_code: int
    is_paid: bool
    is_printed_application_arrived: bool
    is_passed_first_apply: bool
    is_final_submit: bool
    exam_code: str
