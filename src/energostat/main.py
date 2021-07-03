#!/usr/bin/env python

import logging
from logging.config import dictConfig

from flask import Flask, send_from_directory, request, redirect, send_file

from energostat.app import html2xml_bytes
from energostat.utils import GunicornApplication

logger = logging.getLogger('root')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] [%(name)s.%(funcName)s at %(lineno)d] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
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
        'gunicorn': {
            'handlers': ['simple'],
            'level': 'INFO',
        },
        'flask': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'energostat': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['simple'],
        'level': 'DEBUG',
    }
}

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        logger.warning('No file part')
        return redirect('')
    file = request.files['file']
    if file.filename == '':
        logger.warning('No selected file')
        return redirect('')
    if file:
        f_out = html2xml_bytes(file)
        return send_file(
            f_out,
            as_attachment=True,
            attachment_filename='Energostat.zip',
            mimetype='application/zip'
        )
    return redirect('')


def main():
    dictConfig(LOGGING)
    dictConfig(LOGGING)
    logger.info('Start')
    GunicornApplication(app, LOGGING).run()


if __name__ == '__main__':
    main()
