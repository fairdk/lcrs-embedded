"""LCRS embedded CLI

Usage:
  lcrs_embedded [options]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<port> Port number to listen to [default: 8000]
  -d --debug    Turn of debug messages

"""
import logging

from docopt import docopt

from . import __version__, settings

logger = logging.getLogger(__name__)


def main(*args):
    arguments = docopt(
        __doc__,
        version='LCRS embedded CLI v. {}'.format(__version__),
        argv=args or None,
    )
    port = arguments.get('--port', None) or 8000
    port = int(port)
    settings.setup_logging(debug=arguments.get('--debug', False))

    from .server import serve
    serve(port)


if __name__ == '__main__':
    main()
