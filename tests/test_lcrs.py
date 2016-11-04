#!/usr/bin/env python
import logging
import threading
import time

import pytest

from . import utils

logger = logging.getLogger(__name__)


@pytest.fixture
def runserver(scope="session"):
    from lcrs_embedded import server, settings
    settings.setup_logging(debug=True, test=True)
    serve_thread = threading.Thread(
        target=server.serve,
        kwargs={'port': utils.SERVER_TEST_PORT, 'host': utils.SERVER_HOST}
    )
    serve_thread.setDaemon(True)
    serve_thread.start()
    # Wait for server to actually start
    time.sleep(0.1)
    yield
    server.stop()


def test_api(runserver):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    logger.info("Testing the API...")
    utils.request_api_endpoint("/api/v1/test/")
    logger.info("Done with that")
