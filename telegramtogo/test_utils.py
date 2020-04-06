"""
Utils tests.
"""

from telegramtogo.utils import getLoggingLevel

import logging


def testGetLoggingLevel():
    tests = {
        -1: logging.ERROR,
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
        42: logging.DEBUG,
    }
    for verbose, level in tests.items():
        print(verbose, level)
        assert getLoggingLevel(verbose) == level
