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
        'asyncio': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'aiotg': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'assistant': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
    },
}
