from sanic.response import text
from sanic.handlers import ErrorHandler

from exceptions import Conflict


async def conflict_handler(request, exception):
    return text(exception.args[0], exception.status_code)


def add_error_handlers(app):
    app.error_handler.add(Conflict, conflict_handler)
