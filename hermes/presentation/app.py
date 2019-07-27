import os
from sanic import Sanic
from entry_logger_sanic import set_logger

from hermes.misc.config import settings
from hermes.misc.constants import LISTENER_OPTION, LOGO, SERVICE_NAME, RUN_ENV
from hermes.presentation.handler import add_error_handlers
from hermes.presentation.listener import initialize, migrate, release
from hermes.presentation.views.router import bp


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO

    if RUN_ENV == "prod":
        _app.config["SLACK_WEBHOOK_URL"] = settings.SLACK_WEBHOOK_URL
        _app.config["SLACK_MAINTAINER_ID"] = settings.SLACK_MAINTAINER_ID

    log_path = os.path.dirname(__file__).replace("/hermes", "").replace("/presentation", "")

    set_logger(_app, log_path)

    _app.register_listener(initialize, LISTENER_OPTION[0])
    _app.register_listener(migrate, LISTENER_OPTION[0])
    _app.register_listener(release, LISTENER_OPTION[3])

    add_error_handlers(_app)

    _app.blueprint(bp)

    return _app
