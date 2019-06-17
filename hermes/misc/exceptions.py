from sanic.exceptions import SanicException, add_status_code


@add_status_code(409)
class Conflict(SanicException):
    pass


@add_status_code(400)
class BadRequest(SanicException):
    pass


class AdminAlreadyExistException(Exception):
    pass


class AdminNotFoundException(Exception):
    pass


class ApplicantAlreadyExistException(Exception):
    pass


class ApplicantNotFoundException(Exception):
    pass


class ApplicantStatusNotFoundException(Exception):
    pass
