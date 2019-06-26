from dataclasses import dataclass


@dataclass
class ApplicantStatus:
    applicant_email: str
    receipt_code: int
    is_paid: bool
    is_printed_application_arrived: bool
    is_passed_first_apply: bool
    is_final_submit: bool
    exam_code: str
