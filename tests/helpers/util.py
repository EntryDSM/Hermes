import random
import string
import uuid


class DunnoValue:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __eq__(self, other):
        if isinstance(self.expected_type, list):
            return self._list_eq(other)
        else:
            return self._type_eq(other)

    def _list_eq(self, other):
        for expected_type in self.expected_type:
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


def generate_random_string(length: int = 10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_phone_number():
    return f"010{random.randint(1000, 9999)}{random.randint(1000, 9999)}"


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


def status_message_response():
    return {"msg": DunnoValue(str)}
