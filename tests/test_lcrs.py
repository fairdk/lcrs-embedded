#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lcrs_embedded
----------------------------------

Tests for `lcrs_embedded` module.
"""

import pytest

# from lcrs_embedded import cli


@pytest.fixture
def runserver(scope='session'):
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(runserver):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_cli():
    """
    Run basic CLI tests
    """
    # cli.main()
