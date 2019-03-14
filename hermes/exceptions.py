from sanic.exceptions import SanicException, add_status_code


@add_status_code(409)
class Conflict(SanicException):
    pass
