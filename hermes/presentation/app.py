from sanic import Sanic

from hermes.misc.constants import LISTENER_OPTION, LOGO, SERVICE_NAME
from hermes.presentation.handler import add_error_handlers
from hermes.presentation.listener import initialize, release
from hermes.presentation.views.router import bp


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO

    _app.register_listener(initialize, LISTENER_OPTION[0])
    _app.register_listener(release, LISTENER_OPTION[3])

    add_error_handlers(_app)

    _app.blueprint(bp)

    return _app
