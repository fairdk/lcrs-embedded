#!/usr/bin/env python3
import os
import socket
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

HOST = socket.gethostname()


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


CWD = os.getcwd()


def server(port):

    server = ThreadingSimpleServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print("Serving HTTP traffic from", CWD, "on", HOST, "using port", port)
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("\nShutting down server per users request.")
