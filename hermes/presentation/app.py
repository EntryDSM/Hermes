import os
from sanic import Sanic
from entry_logger_sanic import set_logger

from hermes.misc.constants import LISTENER_OPTION, LOGO, SERVICE_NAME
from hermes.presentation.handler import add_error_handlers
from hermes.presentation.listener import initialize, migrate, release
from hermes.presentation.views.router import bp


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO

    log_path = os.path.dirname(__file__).replace("/hermes", "").replace("/presentation", "")

    set_logger(_app, log_path)

    _app.register_listener(initialize, LISTENER_OPTION[0])
    _app.register_listener(migrate, LISTENER_OPTION[0])
    _app.register_listener(release, LISTENER_OPTION[3])

    add_error_handlers(_app)

    _app.blueprint(bp)

    return _app
