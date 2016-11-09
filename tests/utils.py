import logging

import requests
from requests.exceptions import ConnectionError

from .context import assert_no_thread_exceptions

logger = logging.getLogger(__name__)


SERVER_HOST = '127.0.0.1'
SERVER_TEST_PORT = 23452


class WrongStatusCode(AssertionError):
    pass


def get_url(urlpath):
    return "http://{}:{}{}".format(SERVER_HOST, SERVER_TEST_PORT, urlpath)


def request_api_endpoint(urlpath):
    with assert_no_thread_exceptions():
        url = get_url(urlpath)
        logger.debug("Testing API endpoint, url: {}".format(url))
        try:
            response = requests.post(url)
            if not response.status_code == 200:
                raise WrongStatusCode("Status code was {}".format(
                    response.status_code
                ))
            return response
        except ConnectionError:
            raise AssertionError("Server isn't alive")


def compare_dictionaries(dict1, dict2):

    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return False

    shared_keys = set(dict2.keys()) & set(dict2.keys())

    if not (len(shared_keys) == len(dict1.keys()) and
            len(shared_keys) == len(dict2.keys())):
        return False

    dicts_are_equal = True
    for key in dict1.keys():
        if type(dict1[key]) is dict:
            dicts_are_equal = dicts_are_equal and compare_dictionaries(
                dict1[key], dict2[key])
        else:
            dicts_are_equal = dicts_are_equal and (dict1[key] == dict2[key])

    return dicts_are_equal
