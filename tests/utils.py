import logging
import requests


logger = logging.getLogger(__name__)


SERVER_HOST = '127.0.0.1'
SERVER_TEST_PORT = 8989


def get_url(urlpath):
    return "http://{}:{}{}".format(SERVER_HOST, SERVER_TEST_PORT, urlpath)


def request_api_endpoint(urlpath):
    url = get_url(urlpath)
    logger.debug("Testing API endpoint, url: {}".format(url))
    response = requests.post(url)
    assert response.status_code == 200, "Status code was {}".format(
        response.status_code
    )
