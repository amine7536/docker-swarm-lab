# -*- coding: utf-8 -*-

import logging
from logging import Formatter, getLogger, StreamHandler
from colors import Color

logger = logging.getLogger(__name__)


def debug_factory(logger, debug_level):
    """
    Decorate logger in order to add custom levels for Nagios
    :param logger:
    :param debug_level:
    :return: custom_debug function

    Todo: this should be a singleton class
    """
    def custom_debug(msg, *args, **kwargs):
        if logger.level >= debug_level:
            return
        logger._log(debug_level, msg, args, kwargs)
    return custom_debug


colored = Color().colored

class ColoredFormatter(Formatter):
    """
    Setup Colored Formatter
    """
    def format(self, record):

        message = record.getMessage()

        mapping = {
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bgred',
            'DEBUG': 'bggrey',
            'SUCCESS': 'green'
        }

        clr = mapping.get(record.levelname, 'white')

        return colored(record.levelname, clr) + ': ' + message


def setup_logger(verbose=False):
    """
    Setup Logger
    :param logfile:
    :param verbose:
    :return:
    """
    handler = StreamHandler()
    formatter = ColoredFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # set success level
    logging.SUCCESS = 25  # between WARNING and INFO
    logging.addLevelName(logging.SUCCESS, 'SUCCESS')
    setattr(logger, 'success', debug_factory(logger, logging.SUCCESS))
    # setattr(logger, 'success', lambda message, *args: logger._log(logging.SUCCESS, message, args))

    # Logging settings
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s %(message)s', level=log_level)
    logger.setLevel(log_level)

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.info('info')
    logger.success('success')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
