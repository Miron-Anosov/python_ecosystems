import logging.handlers
import datetime
from logging import LogRecord
from os import PathLike
from typing import Optional, Dict


class FileSeparateDebug(logging.Handler):
    """
    Дочерний handler наследуемый от logging.Handler
    Записывает логи исключительно уровня  DEBUG.
    """

    def __init__(self, filename: str, mode: str = Optional[None], encoding: str = 'UTF-8'):
        super().__init__()
        self.file_name: str = filename
        self.mode: str = mode if mode else 'a'
        self.encoding: str = encoding

    def emit(self, record: logging.LogRecord) -> None:
        """
        Обрабатываются логи только уровня DEBUG.
        """
        if record.levelno == 10:
            message: str = self.format(record=record)
            message: str = ''.join(message + '\n')
            with open(file=self.file_name, mode=self.mode, encoding=self.encoding) as log:
                log.write(message)


class FileSeparateError(logging.Handler):
    """
    Дочерний handler наследуемый от logging.Handler
    Записывает логи исключительно уровня ERROR.
    """

    def __init__(self, filename: str, mode: str = Optional[None], encoding: str = 'UTF-8') -> None:
        super().__init__()
        self.file_name: str = filename
        self.mode: str = mode if mode else 'a'
        self.encoding: str = encoding

    def emit(self, record: logging.LogRecord) -> None:
        """
        Обрабатываются логи только уровня ERROR
        """
        if record.levelno == 40:
            message: str = self.format(record=record)
            message: str = ''.join(message + '\n')
            with open(file=self.file_name, mode=self.mode, encoding=self.encoding) as log:
                log.write(message)


class ASCIIFilter(logging.Filter):
    """
    Дочерний фильтр наследуемый от logging.Filter.
    Данный фильтр отвечает за проверку символов таблицы ascii.
    """

    def filter(self, record: logging.LogRecord) -> Optional[bool]:
        """
        Обрабатываются логи только те, которые входят в таблицу ascii.
        """
        value: str = record.msg
        if isinstance(value, str):
            return not any(True if ord(i) > 127 else False for i in value)
# TODO можно сделать проще:
# class AsciiFilter(logging.Filter):
#     def filter(self, record: LogRecord) -> bool:
#         return str.isascii(record.msg)


class HTTPHandlerCustom(logging.handlers.HTTPHandler):
    """
    Дочерний handler наследуемый от logging.handlers.HTTPHandler.
    Передает логи по установленным параметрам.
    """
    def mapLogRecord(self, record: LogRecord) -> Dict:
        """
        Метод формирует словарь согласно предварительно настроенному формату логов.
        """
        created_datetime = datetime.datetime.fromtimestamp(record.created)
        log_data: Dict = {"level": record.levelname,
                          "name log": record.name,
                          "time": created_datetime,
                          "line": record.lineno,
                          "message": record.msg}
        return log_data


class RootStreamHandler(logging.StreamHandler):
    """
    Дочерний handler наследуемый от logging.StreamHandler.
    Записывает логи согласно родительскому классу, но уже с примененным фильтром ASCIIFilter.
    """

    def __init__(self, stream=None) -> None:
        super().__init__(stream=stream)
        self.addFilter(ASCIIFilter())


class UtilTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Дочерний handler наследуемый от logging.handlers.TimedRotatingFileHandler.
    Записывает логи согласно родительскому классу, но уже с примененным фильтром ASCIIFilter.
    """

    def __init__(self, filename: str | PathLike[str], when: str = ..., interval: int = ...,
                 backupCount: int = ..., encoding: str | None = ...) -> None:
        super().__init__(filename=filename, when=when, interval=interval, backupCount=backupCount, encoding=encoding)
        self.addFilter(ASCIIFilter())
