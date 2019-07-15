import logging.config
import os

LEVEL = os.environ.get('LEVEL', 'development')

# Database
DEFAULT_DATABASE = 'currency' if LEVEL != 'test' else 'test_currency'
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', DEFAULT_DATABASE)
DB_USER = os.environ.get('DB_USER', 'currency')
DB_PWD = os.environ.get('DB_PWD', 'currency')

DB_DSN = f'postgres://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DB_CONNECT_RETRY = 10  # amount of retries to establish connection

DB_PARAMS = {
    'dsn': DB_DSN,
    'pool_min_size': 2,
    'pool_max_size': 5,
    'kwargs': {
        'max_inactive_connection_lifetime': 0,
        'command_timeout': 10,
    }
}

# App
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
APP_PORT = os.environ.get('APP_PORT', 8080)

BASIC_AUTH_LOGIN = os.environ.get('BASIC_AUTH_LOGIN', 'user')
# 'password' by default
BASIC_AUTH_PWD_HASH = os.environ.get('BASIC_AUTH_PWD_HASH', '5f4dcc3b5aa765d61d8327deb882cf99')

TEMPLATE_DIR = 'app/templates'

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'gino': {
            'propagate': False,
        }
    }
}
logging.config.dictConfig(LOGGING)
