"""LCRS embedded CLI

Usage:
  lcrs_embedded [--port=<port>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<port> Port number to listen to [default: 8000]
  -d --debug    Turn of debug messages

"""
from __future__ import absolute_import, print_function, unicode_literals

import logging
from logging import config as logging_config

from docopt import docopt

from . import __version__
from .http_server import server

logger = logging.getLogger(__name__)


def setup_logging(debug=False):
    """Configures logging in cases where a Django environment is not supposed
    to be configured"""
    from . import settings
    if debug:
        settings.DEBUG = True
    settings.LOGGING['handlers']['console']['level'] = 'DEBUG'
    settings.LOGGING['loggers']['lcrs_embedded']['level'] = 'DEBUG'
    logging_config.dictConfig(settings.LOGGING)
    logger.debug("Debug mode is on!")


def main():
    arguments = docopt(
        __doc__,
        version='LCRS embedded CLI v. {}'.format(__version__)
    )

    port = arguments.get('--port', None) or 8000

    setup_logging(debug=arguments.get('--debug', False))

    server(port)


if __name__ == '__main__':
    main()
