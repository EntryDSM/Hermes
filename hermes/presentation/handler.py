from sanic import Sanic
from sanic.request import Request
from sanic.response import text

from hermes.misc.exceptions import SanicException


async def base_handler(request: Request, exception: SanicException):
    return text(exception.args[0], exception.status_code)


def add_error_handlers(app: Sanic):
    app.error_handler.add(SanicException, base_handler)
