import logging
import os
import queue
from logging import config as logging_config

__logger = logging.getLogger(__name__)


DEBUG = True

RUNTIME_DATA = "/tmp/lcrs_embedded"

os.makedirs(RUNTIME_DATA, 0o755, True)

HTTP_SRV_PATH = RUNTIME_DATA

EXCEPTION_QUEUE = queue.Queue()


class RequireDebugFalse(logging.Filter):

    def filter(self, record):
        return not DEBUG


class RequireDebugTrue(logging.Filter):

    def filter(self, record):
        return DEBUG


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d '
                '%(message)s'
            )
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'simple_date': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        }
    },
    'filters': {
        'require_debug_true': {
            '()': RequireDebugTrue,
        },
        'require_debug_false': {
            '()': RequireDebugFalse,
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        },
        'file_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(RUNTIME_DATA, 'debug.log'),
            'formatter': 'simple_date',
        },
        'file': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.FileHandler',
            'filename': os.path.join(RUNTIME_DATA, 'lcrs_embedded.log'),
            'formatter': 'simple_date',
        },
    },
    'loggers': {
        'lcrs_embedded': {
            'handlers': ['console', 'file', 'file_debug'],
            'level': 'INFO',
        },
        'tests': {
            'handlers': ['console', 'file', 'file_debug'],
            'level': 'CRITICAL',
        }
    }
}


def setup_logging(debug=False, test=False):
    """Configures logging in cases where a Django environment is not supposed
    to be configured"""
    global DEBUG, LOGGING
    if debug:
        DEBUG = True
        LOGGING['handlers']['console']['level'] = 'DEBUG'
        LOGGING['loggers']['lcrs_embedded']['level'] = 'DEBUG'
    if test:
        LOGGING['handlers']['console']['level'] = 'DEBUG'
        LOGGING['loggers']['tests']['level'] = 'DEBUG'
    logging_config.dictConfig(LOGGING)
    __logger.debug("Debug mode is on!")
