import json
import logging
import time
from threading import ThreadError

import pytest
from lcrs_embedded import protocol

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
    response = utils.request_api_as_json("/api/v1/status/")
    assert response['state_id'] == protocol.STATE_IDLE


def test_status_busy_api(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing the API status...")

    job_duration = 3

    response = utils.request_api_as_json(
        "/api/v1/wait/",
        data={'wait_time': job_duration},
    )
    job_id = response['job_id']
    assert job_id > 0

    for i in range(job_duration):
        status = utils.request_api_as_object(
            "/api/v1/status/",
            data={'job_id': job_id},
        )
        assert status.job_response.progress <= i
        time.sleep(i)


def test_api_json_in_post_data(runserver):
    """
    This test ensures that we keep support having data=<json data> as the
    request body for a POST request.
    """
    logger.info("Testing the API status...")

    response = utils.request_api_endpoint(
        "/api/v1/status/?json_param=data",
        raw_body={'data': json.dumps({'job_id': 3})},
    )
    json_response = json.loads(response.content.decode("utf-8"))
    job_response = json_response['job_response']
    assert job_response['job_id'] > 0
    assert job_response['status'] == protocol.JOB_UNKNOWN


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
    job = utils.request_api_as_object("/api/v1/scan/")
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


def test_debug_index(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing index page...")
    response = utils.request_get("/")
    response = response.content.decode("utf-8")
    assert "<title>" in response


def test_404(runserver):
    """
    Calls the failing API endpoint, which should catch an exception in the
    remote thread.
    """
    logger.info("Testing debug log...")
    with pytest.raises(utils.WrongStatusCode):
        response = utils.request_get("/does not exist")
        assert response.status_code == 404
