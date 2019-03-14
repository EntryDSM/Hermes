from sanic.response import text

from exceptions import Conflict, BadRequest


async def base_handler(request, exception):
    return text(exception.args[0], exception.status_code)


def add_error_handlers(app):
    app.error_handler.add(Conflict, base_handler)
    app.error_handler.add(BadRequest, base_handler)
