#!/usr/bin/env python3
import json
import logging
import sys

from . import __version__, settings
from .utils.http import JSONRequestHandler, ThreadingSimpleServer

logger = logging.getLogger(__name__)


__active = True


class LCRSRequestHandler(JSONRequestHandler):
    server_version = "LCRS/" + __version__
    static_srv = settings.HTTP_SRV_PATH

    def api_test(self, **kwargs):
        logger.debug('api_test called, kwargs: {}'.format(kwargs))
        self.respond(
            content_type="application/json",
            body=json.dumps({'OK': "Hej"}),
        )


def serve(port=8000, host='0.0.0.0'):
    global __active
    server = ThreadingSimpleServer(('0.0.0.0', port), LCRSRequestHandler)
    logger.info(
        "Serving HTTP traffic on http://{host}:{port}".format(
            host=host, port=port
        )
    )
    try:
        while __active:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        logger.info(
            "User stopped server"
        )


def stop():
    global __active
    logger.info(
        "Asking HTTP server to stop"
    )
    __active = False
