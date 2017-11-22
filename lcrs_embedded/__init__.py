# -*- coding: utf-8 -*-
import sys

__author__ = """Benjamin Bach"""
__email__ = 'benjamin@fairdanmark.dk'
__version__ = '1.0dev'

if sys.version_info < (3, 4, 0):
    raise RuntimeError("Ricecooker only supports Python 3.4+")
