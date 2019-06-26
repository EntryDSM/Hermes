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
