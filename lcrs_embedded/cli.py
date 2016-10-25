"""LCRS embedded CLI

Usage:
  lcrs_embedded [--port=<port>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<port> Port number to listen to [default: 8000]

"""
from __future__ import absolute_import, print_function, unicode_literals

from docopt import docopt

from . import __version__
from .http_server import server


def main():
    arguments = docopt(
        __doc__,
        version='LCRS embedded CLI v. {}'.format(__version__)
    )

    port = arguments.get('--port', None) or 8000

    server(port)


if __name__ == '__main__':
    main()
