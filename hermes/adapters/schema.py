import re
from typing import Any, List

from marshmallow import EXCLUDE
from marshmallow import Schema as BaseSchema
from marshmallow import post_load
from marshmallow.fields import Boolean, Date, Email, Integer
from marshmallow.fields import String as BaseString

from hermes.entities.admin import Admin
from hermes.entities.applicant import Applicant, ApplicantStatus


class String(BaseString):
    def __init__(self, length=None, regex=None, **kwargs):
        length_validation = (lambda s: len(s) <= length) if length else (lambda s: True)
        validation = (
            (lambda s: re.match(regex, s) and length_validation(s))
            if regex
            else length_validation
        )
        super().__init__(validate=validation, **kwargs)


class Enum(BaseString):
    def __init__(self, enum: List[str], **kwargs):
        validation = lambda s: s in enum
        super().__init__(validate=validation, **kwargs)


class Schema(BaseSchema):
    __entity__: Any

    class Meta:
        unknown = EXCLUDE

    @post_load
    def deserialize(self, data):
        return self.__entity__(**data)


class AdminSchema(Schema):
    __entity__ = Admin

    admin_id = String(required=True, allow_none=False, length=45)
    admin_password = String(required=True, allow_none=False, length=93)
    admin_type = Enum(
        required=True, allow_none=False, enum=["ROOT", "ADMINISTRATION", "INTERVIEW"]
    )
    admin_email = Email(required=True, allow_none=False)
    admin_name = String(required=True, allow_none=False, length=13)


class AdminPatchSchema(Schema):
    __entity__ = Admin

    admin_id = String(required=False, allow_none=False, length=45)
    admin_password = String(required=False, allow_none=False, length=93)
    admin_type = Enum(
        required=False, allow_none=False, enum=["ROOT", "ADMIN", "INTERVIEW"]
    )
    admin_email = Email(required=False, allow_none=False)
    admin_name = String(required=False, allow_none=False, length=13)


class ApplicantSchema(Schema):
    __entity__ = Applicant

    email = Email(required=True, allow_none=False)
    password = String(required=True, allow_none=False, length=93)
    applicant_name = String(missing=None, length=13)
    sex = Enum(missing=None, enum=["MALE", "FEMALE"])
    birth_date = Date(missing=None)
    parent_name = String(missing=None, length=13)
    parent_tel = String(missing=None, regex=r"01\d-\d{3,4}-\d{4}")
    applicant_tel = String(missing=None, regex=r"01\d-\d{3,4}-\d{4}")
    address = String(missing=None, length=500)
    post_code = String(missing=None, length=5)
    image_path = String(missing=None, length=256)


class ApplicantStatusSchema(Schema):
    __entity__ = ApplicantStatus

    applicant_email = Email(required=True, allow_none=False)
    receipt_code = Integer(missing=None)
    is_paid = Boolean(missing=False)
    is_printed_application_arrived = Boolean(missing=False)
    is_passed_first_apply = Boolean(missing=False)
    is_final_submit = Boolean(missing=False)
    exam_code = String(length=6)
