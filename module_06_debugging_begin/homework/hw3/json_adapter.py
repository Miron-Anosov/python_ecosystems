"""
Удобно сохранять логи в определённом формате, чтобы затем их можно было фильтровать и анализировать. 
Сконфигурируйте логгер так, чтобы он писал логи в файл skillbox_json_messages.log в следующем формате:

{"time": "<время>", "level": "<уровень лога>", "message": "<сообщение>"}

Но есть проблема: если в message передать двойную кавычку, то лог перестанет быть валидной JSON-строкой:

{"time": "21:54:15", "level": "INFO", "message": "“"}

Чтобы этого избежать, потребуется LoggerAdapter. Это класс из модуля logging,
который позволяет модифицировать логи перед тем, как они выводятся.
У него есть единственный метод — process, который изменяет сообщение или именованные аргументы, переданные на вход.

class JsonAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    # меняем msg
    return msg, kwargs

Использовать можно так:

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Сообщение')

Вам нужно дописать метод process так, чтобы в логах была всегда JSON-валидная строка.
"""
import json
import logging
import os.path
from logging import Formatter, FileHandler, StreamHandler


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        new_message: str = msg
        new_message: str = json.dumps(new_message, ensure_ascii=False).replace(r'\"', '"')
        return new_message, kwargs


if __name__ == '__main__':
    path_file: str = os.path.abspath(os.path.join('skillbox_json_messages.log'))
    logger: JsonAdapter = JsonAdapter(logging.getLogger(__name__))

    formatter: Formatter = logging.Formatter(
        fmt='{"time" : "%(asctime)s",  "level" : "%(levelname)s",  "message" : %(message)s}', datefmt="%H:%M:%S")
    file_handler: FileHandler = logging.FileHandler(filename=path_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(fmt=formatter)
    file_handler.setLevel(level=logging.DEBUG)
    logger.logger.addHandler(file_handler)

    ch: StreamHandler = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(fmt=formatter)
    logger.logger.addHandler(ch)

    logger.setLevel(logging.DEBUG)
    logger.info('Сообщение')
    logger.error('Кавычка)"')
    logger.debug("Еще одно ""'сообщение'")
