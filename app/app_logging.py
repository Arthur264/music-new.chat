import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - (%(name)s)[%(levelname)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'access': {
            'format': '%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'logstash': {
            '()': 'logstash_formatter.LogstashFormatter'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
        },
        'internal': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stderr
        },
        'accessStream': {
            'class': 'logging.StreamHandler',
            'formatter': 'access',
            'stream': sys.stderr
        },

        'internalFile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filters': ['statusFilter', 'emptyFilter'],
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'filename': 'log/current.log',
        },
        'accessFile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'access',
            'filters': ['statusFilter', 'emptyFilter'],
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'filename': 'log/current.log',
        },

        'logstash': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 2,
            'formatter': 'logstash',
            'filters': ['statusFilter', 'emptyFilter'],
            'filename': 'log/logstash.log',
        },

    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['internal', 'internalFile', 'logstash']
        },
        'root': {
            'level': 'INFO',
            'handlers': ['internal', 'internalFile'],
            'propagate': False
        },
        "sanic.error": {
            "level": "INFO",
            "handlers": ['internal', 'internalFile'],
            "propagate": False,
            "qualname": "sanic.error"
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ['accessStream', 'accessFile'],
            "propagate": False,
            "qualname": "sanic.access"
        },
    }
}
