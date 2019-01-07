#!/usr/bin/env python

import logging
from logging.config import dictConfig

from energostat.app import html2xml

logger = logging.getLogger('root')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)-5s [%(asctime)s, %(msecs)d] %(name)s.%(funcName)s at %(lineno)d: %(message)s',
            'datefmt': '%Y-%b-%d %H:%M:%S',
        },
    },
    'handlers': {
        'simple': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'energostat': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'root': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
    },
}


def main():
    dictConfig(LOGGING)
    logger.info('Starting app')

    with open('tmp/sensors.zip', 'rb') as f_in, open('tmp/messages.zip', 'wb') as f_out:
        html2xml(f_in, f_out)


if __name__ == '__main__':
    main()
