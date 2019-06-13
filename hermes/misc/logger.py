import os
import json
import logging
import traceback
from datetime import datetime

from sanic import Sanic, request, response
from sanic.log import logger as sanic_logger

from hermes.misc.constants import SERVICE_NAME


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "level": record.levelname,
            "issued_at": _iso_time_format(datetime.utcnow()),
            "logger": record.name,
            "thread": record.threadName,
            "module": record.module,
            "filename": record.filename,
            "line_no": record.lineno,
            "msg": record.getMessage(),
            "exec_info": ''.join(traceback.format_exception(*record.exc_info)) if record.exc_info else ''
        }
        return json.dumps(log)


def _create_handler(log_path, formatter=None):
    handler = logging.FileHandler(f"{log_path}/{SERVICE_NAME}.log")
    handler.setFormatter(formatter)

    return handler


def _iso_time_format(dt):
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, int(dt.microsecond / 1000))


def set_logger(app: Sanic):
    if not isinstance(app, Sanic):
        raise RuntimeError("Invalid app was given")

    log_path = os.path.dirname(__file__).replace("/hermes", "").replace("/misc", "")
    sanic_logger.info(f"Service log will saved at {os.path.abspath(f'{log_path}/{SERVICE_NAME}.log')}")

    _set_sanic_logger(log_path)
    logger = _set_request_logger(log_path)

    @app.middleware("request")
    def request_log(req: request.Request):
        req["request_time"] = datetime.utcnow()

    @app.middleware("response")
    def response_log(req: request.Request, res: response.HTTPResponse):
        log = {
            "level": "INFO" if res.status == 200 else "WARN",
            "issued_at": _iso_time_format(req["request_time"]),
            "url": req.url,
            "method": req.method,
            "path": req.path,
            "path_template": req.uri_template,
            "request_header": dict(req.headers),
            "request_body": req.body.decode(),
            "request_query_string": req.args,
            "request_ip": req.ip,
            "request_received_at": _iso_time_format(req["request_time"]),
            "response_sent_at": _iso_time_format(datetime.utcnow()),
            "response_status": res.status,
            "response_content_type": res.content_type,
            "response_body": res.body.decode(),
            "response_body_length": len(res.body),
            "duration_time": str(req["request_time"] - datetime.utcnow())
        }
        logger.info(json.dumps(log))


def _set_sanic_logger(log_path):
    handler = _create_handler(log_path, JSONLogFormatter())

    sanic_logger.addHandler(handler)


def _set_request_logger(log_path):
    handler = _create_handler(log_path)

    logger = logging.getLogger("sanic-request-log")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
