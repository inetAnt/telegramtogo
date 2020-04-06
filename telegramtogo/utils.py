"""
Utils
"""
import logging


def getLoggingLevel(verbosity):
    """Verbosity level to logging level."""
    logLevels = {0: logging.WARNING, 1: logging.INFO}
    if verbosity > 1:
        return logging.DEBUG
    else:
        return logLevels.get(verbosity, logging.ERROR)
