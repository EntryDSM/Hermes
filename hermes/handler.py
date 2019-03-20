from sanic.response import text

from hermes.exceptions import SanicException


async def base_handler(request, exception):
    return text(exception.args[0], exception.status_code)


def add_error_handlers(app):
    app.error_handler.add(SanicException, base_handler)
