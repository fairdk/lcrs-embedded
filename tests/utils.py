import logging
import requests
from .context import assert_no_thread_exceptions


logger = logging.getLogger(__name__)


SERVER_HOST = '127.0.0.1'
SERVER_TEST_PORT = 8988


class WrongStatusCode(AssertionError):
    pass


def get_url(urlpath):
    return "http://{}:{}{}".format(SERVER_HOST, SERVER_TEST_PORT, urlpath)


def request_api_endpoint(urlpath):
    with assert_no_thread_exceptions():
        url = get_url(urlpath)
        logger.debug("Testing API endpoint, url: {}".format(url))
        response = requests.post(url)
        if not response.status_code == 200:
            raise WrongStatusCode("Status code was {}".format(
                response.status_code
            ))
