#!/usr/bin/env python3
import json
import logging
import sys

from . import __version__, settings
from .utils.http import JSONRequestHandler, ThreadingSimpleServer

logger = logging.getLogger(__name__)


class LCRSRequestHandler(JSONRequestHandler):
    server_version = "LCRS/" + __version__
    static_srv = settings.HTTP_SRV_PATH

    def api_test(self, **kwargs):
        logger.debug('api_test called, kwargs: {}'.format(kwargs))
        self.respond(
            content_type="application/json",
            body=json.dumps({'OK': "Hej"}),
        )


def server(port):

    host = '0.0.0.0'  # socket.gethostname()

    server = ThreadingSimpleServer(('0.0.0.0', port), LCRSRequestHandler)
    logger.info(
        "Serving HTTP traffic on http://{host}:{port}".format(
            host=host, port=port
        )
    )
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("\nShutting down server per users request.")
