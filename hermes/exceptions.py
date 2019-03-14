from sanic.exceptions import SanicException, add_status_code, NotFound


@add_status_code(409)
class Conflict(SanicException):
    pass

@add_status_code(400)
class BadRequest(SanicException):
    pass
