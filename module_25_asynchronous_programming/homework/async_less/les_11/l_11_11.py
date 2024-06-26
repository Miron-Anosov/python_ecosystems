# API загрузки файла на сервер
import asyncio
from asyncio import StreamReader, StreamWriter


class FileUpload:
    def __init__(self,
                 reader: StreamReader,
                 writer: StreamWriter):
        self._reader = reader
        self._writer = writer
        self._finished_event = asyncio.Event()
        self._buffer = b''
        self._upload_task = None

    def listen_for_uploads(self):
        # Создаем задачу, которая читает данные
        self._upload_task = asyncio.create_task(self._accept_upload())

    async def _accept_upload(self):
        # Читаем данные и отправляем их в буфер.
        while data := await self._reader.read(1024):
            self._buffer = self._buffer + data
        self._finished_event.set()  # Объявляем ивент законченным.
        self._writer.close()  # вызываем закрытие стрима записи
        await self._writer.wait_closed()

    async def get_contents(self):
        """Блокирует событие пока событие не будет выполнено. После чего возвращаем буфер."""
        await self._finished_event.wait()
        return self._buffer


