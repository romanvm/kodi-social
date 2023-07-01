import logging.config
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / 'kodi-social.log'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(message)s',
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_FILE),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'default',
        },
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'log_file']
        },
        'kodi-social': {
            'level': 'DEBUG',
            'handlers': ['console', 'log_file'],
            'propagate': False,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


def get_logger():
    return logging.getLogger('kodi-social')
