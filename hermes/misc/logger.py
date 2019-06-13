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


def _iso_time_format(dt):
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, int(dt.microsecond / 1000))

