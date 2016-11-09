import pytest
import threading
import time


from . import utils

__all__ = ['runserver']


@pytest.fixture
def runserver(scope="module"):
    from lcrs_embedded import server, settings
    settings.setup_logging(debug=True, test=True)
    utils.SERVER_TEST_PORT += 1
    port = utils.SERVER_TEST_PORT
    serve_thread = threading.Thread(
        target=server.serve,
        kwargs={'port': port, 'host': utils.SERVER_HOST}
    )
    serve_thread.setDaemon(True)
    serve_thread.start()
    # Wait for server to actually start
    time.sleep(0.1)
    yield
    server.stop(port)
