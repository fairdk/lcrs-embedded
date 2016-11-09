import json
import logging
import os
import posixpath
import re
import select
import sys
import urllib
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pkg_resources

logger = logging.getLogger(__name__)


class SimpleServer(HTTPServer):

    lcrs_state = "IDLE"

    def handle_error(self, request, client_address):
        HTTPServer.handle_error(self, request, client_address)
        # Exception in request handling, we quit
        sys.exit(123)


class JSONRequestHandler(SimpleHTTPRequestHandler):

    # Make rfile unbuffered -- we need to read one line and then pass
    # the rest to a subprocess, so we can't use buffered input.
    rbufsize = 0

    static_srv = "/path/to/static/files"

    # Example: /api/v1/format-drive/force/
    api_url_scheme = r"/api/v([0-9]+)/(?P<command>.+)/(?P<flags>.*)"

    def respond(
        self,
        body="",
        content_type="text/html",
        charset="utf-8",
        content_length=0,
        status=HTTPStatus.OK
    ):
        if not content_length:
            content_length = len(body)
        logger.debug("Sending response: {}".format(body[:200]))
        self.send_response(status)
        self.send_header(
            "Content-Type",
            "{ct}; charset={charset}".format(ct=content_type, charset=charset)
        )
        self.send_header("Content-Length", str(content_length))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
        self.wfile.flush()
        self.connection.close()

    def log_message(self, fmt, *args):
        logger.debug("{addr} {dtm} - {msg}".format(
            addr=self.address_string(),
            dtm=self.log_date_time_string(),
            msg=fmt % args
        ))

    def do_GET(self):
        """Serve a GET request."""

        debug_url_path = "/debug"

        if self.path == "/":
            index_page = pkg_resources.resource_filename(  # @UndefinedVariable
                'lcrs_embedded',
                os.path.join('data', 'index.html')
            )
            response = open(index_page, "r").read()
            self.respond(
                content_length=len(response),
                body=response
            )

        elif self.path.startswith(""):
            if self.path.startswith(debug_url_path):
                self.path = self.path[len(debug_url_path):]
            if self.path.startswith("//"):
                self.path = self.path[1:]
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_POST(self):

        url_match = re.compile(self.api_url_scheme).search(self.path)

        if not url_match:
            self.respond(
                content_type="application/json",
                body=json.dumps({'fail': "invalid request"}),
                status=HTTPStatus.FORBIDDEN
            )
            return

        command_name = url_match.group('command')

        command_callable = getattr(self, 'api_{}'.format(command_name), None)
        if not command_callable:
            logger.error("Invalid command ID: {}".format(command_name))
            self.respond(
                content_type="application/json",
                body=json.dumps({'fail': "invalid command ID"}),
                status=HTTPStatus.FORBIDDEN
            )
            return

        length = int(self.headers.get('Content-Length'))
        try:
            nbytes = int(length)
        except (TypeError, ValueError):
            nbytes = 0

        if self.command.lower() == "post" and nbytes > 0:
            data = self.rfile.read(nbytes)
        else:
            data = None

        # throw away additional data [see bug #427345]
        while select.select([self.rfile._sock], [], [], 0)[0]:
            if not self.rfile._sock.recv(1):
                break

        data = urllib.parse.parse_qs(data)

        kwargs = json.loads(data['data'][0]) if 'data' in data else {}

        flags = (url_match.group('flags') or "")
        flags = flags.split("/")
        flags = filter(lambda x: bool(x), flags)

        for flag in flags:
            kwargs[flag] = True

        command_callable(**kwargs)

        return

    def translate_path(self, path):
        """
        It was necessary to copy this whole method to avoid using os.getcwd
        and thus avoid being dependent on the cwd for serving static files
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.static_srv
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path
