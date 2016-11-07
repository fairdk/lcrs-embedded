import pytest
import threading
import time


from . import utils

__all__ = ['runserver']


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
