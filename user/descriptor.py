import re
import datetime
import uuid
from typing import Iterable

from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash


class Type:
    name: str

    def __init__(self, default=None, allow_none=True):
        self.default = default
        self.allow_none = allow_none

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Integer(Type):
    def __init__(self, unsigned=False, default=None, allow_none=True):
        self.unsigned = unsigned
        if default:
            if not isinstance(default, int):
                raise ValueError(f"int was expected for default but {type(default)} was given")
            if self.unsigned:
                if default < 0:
                    raise ValueError("expected positive for default but negative was given")
        super(Integer, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Integer, self).__set__(instance, value)
            return

        if not isinstance(value, int):
            raise ValueError(f"int was expected but {type(value)} was given")
        if self.unsigned:
            if value < 0:
                raise ValueError("expected positive but negative was given")
        super(Integer, self).__set__(instance, value)


class Float(Type):
    def __init__(self, unsigned=False, default=None, allow_none=True):
        self.unsigned = unsigned
        if default:
            if not isinstance(default, float):
                raise ValueError(f"int was expected for default but {type(default)} was given")
            if self.unsigned:
                if default < 0:
                    raise ValueError("positive was expected but negative was given")
        super(Float, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Float, self).__set__(instance, value)
            return

        if not isinstance(value, float):
            raise ValueError(f"int was expected for default but {type(value)} was given")
        if self.unsigned:
            if value < 0:
                raise ValueError("positive was expected but negative was given")
        super(Float, self).__set__(instance, value)


class String(Type):
    def __init__(self, length=0, default=None, regex=None, allow_none=True):
        self.length = length
        self.regex = regex

        if default:
            if not isinstance(default, str):
                raise ValueError(f"str was expected for default but {type(default)} was given")
            if self.length and (len(default) > self.length):
                raise ValueError(f"maximum length is {self.length} but given string's length is {len(default)}")
            if self.regex:
                if not re.match(regex, default):
                    raise ValueError("given string is not matched with regex")

        super(String, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(String, self).__set__(instance, value)
            return

        if not isinstance(value, str):
            raise ValueError(f"str was expected for default but {type(value)} was given")
        if self.length and (len(value) > self.length):
            raise ValueError(f"maximum length is {self.length} but given string's length is {len(value)}")
        if self.regex:
            if not re.match(self.regex, value):
                raise ValueError("given string is not matched with regex")

        super(String, self).__set__(instance, value)


class Enum(Type):
    keys: Iterable[str]

    def __init__(self, default=None, allow_none=True):
        if default and default not in self.keys:
            raise ValueError(f"default value must be one of {self.keys} but '{default}' was given")
        super(Enum, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Enum, self).__set__(instance, value)
            return
        if value not in self.keys:
            raise ValueError(f"value must be one of {self.keys} but '{value}' was given")
        super(Enum, self).__set__(instance, value)


class Bool(Type):
    def __init__(self, default=None, allow_none=True):
        if default:
            if not isinstance(default, bool):
                raise ValueError(f"bool was expected for default but {type(default)} was given")
        super(Bool, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Bool, self).__set__(instance, value)
            return

        if not isinstance(value, bool):
            raise ValueError(f"bool was expected  but {type(value)} was given")
        super(Bool, self).__set__(instance, value)


class TimeStamp(Type):
    def __init__(self, default=None, allow_none=True):
        if default:
            if not isinstance(default, datetime.datetime):
                raise ValueError(f"datetime was expected for default but {type(default)} was given")
            if callable(default):
                default = default()
        super(TimeStamp, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(TimeStamp, self).__set__(instance, value)
            return

        if not isinstance(value, datetime.datetime):
            raise ValueError(f"datetime was expected but {type(value)} was given")
        super(TimeStamp, self).__set__(instance, value)


class Date(Type):
    def __init__(self, default=None, allow_none=True):
        if default:
            if not isinstance(default, datetime.date):
                raise ValueError(f"date was expected for default but {type(default)} was given")
            if callable(default):
                default = default()
            super(Date, self).__init__(default, allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Date, self).__set__(instance, value)
            return

        if not isinstance(value, datetime.date):
            raise ValueError(f"date was expected but {type(value)} was given")
        super(Date, self).__set__(instance, value)


class UUID(Type):
    def __init__(self, allow_none=True):
        super(UUID, self).__init__(default=uuid.uuid4().hex, allow_none=allow_none)

    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(UUID, self).__set__(instance, value)
            return

        if isinstance(value, uuid.UUID):
            super(UUID, self).__set__(instance, value.hex)
            return
        elif isinstance(value, str):
            try:
                value = uuid.UUID(value)
            except Exception as e:
                raise ValueError("given value is not valid UUID string")
            super(UUID, self).__set__(instance, value.hex)
        else:
            raise ValueError("given value is not neither UUID string nor object")

    def __get__(self, instance, owner):
        uuid_string = super(UUID, self).__get__(instance, owner)
        return uuid.UUID(uuid_string)


class Email(String):
    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Email, self).__set__(instance, value)
            return

        if not isinstance(value, str):
            raise ValueError(f"str was expected for default but {type(value)} was given")
        if self.length and (len(value) > self.length):
            raise ValueError(f"maximum length is {self.length} but given string's length is {len(value)}")
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
            raise ValueError(f"given string is not valid email address")
        if not validate_email(value, check_mx=True):
            raise ValueError(f"given email's domain does not exist")
        super(String, self).__set__(instance, value)


class Password(Type):
    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(Password, self).__set__(instance, value)
            return

        if not isinstance(value, str):
            raise ValueError(f"str was expected for default but {type(value)} was given")
        hashed_pw = generate_password_hash(value)
        super(Password, self).__set__(instance, hashed_pw)


class PhoneNumber(Type):
    def __set__(self, instance, value):
        if self.allow_none and value is None:
            super(PhoneNumber, self).__set__(instance, value)
            return

        if not isinstance(value, str):
            raise ValueError(f"str was expected for default but {type(value)} was given")
        if not re.match(r"01[0-9]-[0-9]{3,4}-[0-9]{4}", value):
            if not re.match(r"0[0-9]{1,2}-[0-9]{3,4}-[0-9]{4}", value):
                raise ValueError("given string is not valid phone number")
        super(PhoneNumber, self).__set__(instance, value)


class AdminEnum(Enum):
    def __init__(self):
        keys = ('ROOT', 'ADMIN', 'INTERVIEW')
        super(AdminEnum, self).__init__(keys)


class SexEnum(Enum):
    def __init__(self):
        keys = ('MALE', 'FEMALE')
        super(SexEnum, self).__init__(keys)
