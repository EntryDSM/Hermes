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

