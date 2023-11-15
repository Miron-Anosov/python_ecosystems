import os.path
import sys
import logging.config

import logging_tree

# from CustomLog import FileSeparateDebug, FileSeparateError
from log_config import log_config
from utils import string_to_operator


def base_config_log() -> None:
    """
    Создается конфигурация logger.
    """
    # logger_root = logging.getLogger()
    # fmt = logging.Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s')
    #
    # sh_stdout = logging.StreamHandler(stream=sys.stdout)
    # sh_stdout.setFormatter(fmt=fmt)
    # sh_stdout.setLevel(level=logging.DEBUG)
    #
    # fh_debug = FileSeparateDebug(file_name='calc_debug.log', mode='a')
    # fh_debug.setFormatter(fmt=fmt)
    # fh_debug.setLevel(level=logging.DEBUG)
    #
    # fh_error = FileSeparateError(file_name='calc_error.log', mode='a')
    # fh_error.setFormatter(fmt=fmt)
    # fh_error.setLevel(level=logging.ERROR)
    #
    # logger_root.addHandler(hdlr=fh_error)
    # logger_root.addHandler(hdlr=fh_debug)
    # logger_root.addHandler(hdlr=sh_stdout)
    # logger_root.setLevel(level=logging.DEBUG)

    # logging.config.dictConfig(log_config)
    path = os.path.abspath(os.path.join('logging_conf.ini'))
    logging.config.fileConfig(fname=path, disable_existing_loggers=False)


base_config_log()
logger = logging.getLogger('app')
logger_http = logging.getLogger('app.http')


def show_and_write_logging_tree() -> None:
    """
     Вывод и запись иерархии логгеров.
    """
    logging_tree.printout()
    with open(file='logging_tree.txt', mode='w', encoding='UTF-8') as tree_file:
        default_stdout = sys.stdout
        sys.stdout = tree_file
        logging_tree.printout()
        sys.stdout = default_stdout


def calc(args):
    logger.root.info('Start calculate. ---test ascii True---')  # Будет выводиться.
    logger.debug(f'Arguments: {args}')

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error(f"Error while converting number 1 : {num_1}")
        logger.exception(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error(f"Error while converting number 2 : {num_2}")
        logger.exception(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.debug(f"{num_1} {operator} {num_2} = {result}")
    logger.info(f'Result: {result}')
    logger.root.info('Close calculatе. ---test аscii False---')  # не будет выводиться, перехватит фильтр.
    logger_http.info('Function calc() was completed')


if __name__ == '__main__':
    show_and_write_logging_tree()
    calc(sys.argv[1:])
