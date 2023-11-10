import os.path
import sys
from CustomHandlers import FileSeparateDebug, FileSeparateError, ASCIIFilter, HTTPHandlerCustom

calc_debug = os.path.abspath(os.path.join('calc_debug.log'))
calc_error = os.path.abspath(os.path.join('calc_error.log'))
utils_info = os.path.abspath(os.path.join('util.log'))
formatter = '%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s'

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': formatter,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'stream': {  # handler для app.py
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': sys.stdout,
            'formatter': 'base'
        },
        'stream_root': {  # handler для root
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'stream': sys.stdout,
            'formatter': 'base',
            'filters': ['ascii']
        },
        'file_error': {  # handler для app.py
            '()': FileSeparateError,  # пишет сообщения исключительно error level
            'level': 'ERROR',
            'filename': calc_error,
            'mode': 'a',
            'formatter': 'base',
            'encoding': 'UTF-8',
        },
        'file_debug': {  # handler для app.py
            '()': FileSeparateDebug,  # пишет сообщения исключительно debug level
            'level': 'DEBUG',
            'filename': calc_debug,
            'mode': 'a',
            'formatter': 'base',
            'encoding': 'UTF-8',
        },
        'file_info_utils': {  # handler для utils.py
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'H',
            'interval': 10,
            'level': 'INFO',
            'filename': utils_info,
            'encoding': 'UTF-8',
            'formatter': 'base',
            'backupCount': 3,
            'filters': ['ascii']
        },
        'http_handler': {
            '()': HTTPHandlerCustom,
            'host': '127.0.0.1:3000',
            'url': '/log',
            'method': 'POST',
            'formatter': 'base',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'app': {  # logger обрабатывает сообщения из модуля app.py
            'level': 'DEBUG',
            'handlers': ['stream', 'file_error', 'file_debug'],
            'propagate': False,
        },
        'app.utils': {  # logger обрабатывает сообщения из модуля utils.py
            'level': 'INFO',
            'propagate': False,
            'handlers': ['file_info_utils'],
        },
        'app.http': {
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['http_handler'],
        },
        'flask': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['stream_root'],
        },
    },
    'root': {
        'formatter': 'base',
        'stream': sys.stdout,
        'level': 'DEBUG',
        'handlers': ['stream_root']
    },
    'filters': {
        'ascii': {
            '()': ASCIIFilter  # фильтр включает символы таблицы ascii
        },
    },

}
