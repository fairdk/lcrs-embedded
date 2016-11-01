#!/usr/bin/env python
import logging
import threading
import time

import pytest
from lcrs_embedded import cli, http_server

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def runserver():
    cli.setup_logging(debug=True)
    serve_thread = threading.Thread(
        target=http_server.serve,
        kwargs={'port': 8989}
    )
    serve_thread.setDaemon(True)
    serve_thread.start()
    yield
    http_server.stop()


def test_api(runserver):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    logger.info("Testing the API...")
    time.sleep(2)
    logger.info("Done with that")
