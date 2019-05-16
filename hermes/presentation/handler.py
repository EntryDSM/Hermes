from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from hermes.misc.exceptions import SanicException


async def base_handler(request: Request, exception: SanicException):
    # pylint: disable=unused-argument
    return json(
        body={
            "msg": exception.args[0]
        },
        status=exception.status_code
    )


def add_error_handlers(app: Sanic):
    app.error_handler.add(SanicException, base_handler)
