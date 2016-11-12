import json
import logging
from threading import ThreadError

import pytest
from lcrs_embedded.utils.models import decoder

from . import *  # noqa  # This loads the fixtures that are in __init__.py
from . import utils


logger = logging.getLogger(__name__)


def test_nonexisting_api(runserver):
    """
    Sample pytest test function with the pytest fixture as an argument.
    """
    logger.info("Testing the API...")
    with pytest.raises(utils.WrongStatusCode):
        utils.request_api_endpoint("/api/v1/doesnotexist/")


def test_status_api(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing the API status...")
    response = utils.request_api_endpoint("/api/v1/status/")
    response = response.content.decode("utf-8")
    assert json.loads(response)['state_id'] == "IDLE"


def test_fail_api(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing the API...")
    with pytest.raises(ThreadError):
        utils.request_api_endpoint("/api/v1/fail/")


def test_scan_api(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing the API status...")
    response = utils.request_api_endpoint("/api/v1/scan/")
    response = response.content.decode("utf-8")
    job = json.loads(response, object_hook=decoder)
    assert job.job_id > 0


def test_debug_log(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing debug log...")
    response = utils.request_get("/debug/")
    response = response.content.decode("utf-8")
    assert "INFO" in response


def test_404(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing debug log...")
    with pytest.raises(utils.WrongStatusCode):
        response = utils.request_get("/does not exist")
        assert response.status_code == 404
