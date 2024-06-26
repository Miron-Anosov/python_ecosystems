# Листинг 8.3 Отправка HTTP-запроса с помощью потоковых писателей и читателей

import asyncio
from asyncio import StreamReader
from typing import AsyncGenerator


async def read_until_empty(stream_reader: StreamReader) -> AsyncGenerator[str, None]:
    while response := await stream_reader.readline():
        yield response.decode()


async def main():
    url = 'www.example.com'
    request: str = f"GET / HTTP/1.1\r\n" \
                   f"Connection: close\r\n" \
                   f"Host: {url}\r\n\r\n"

    stream_reader, stream_writer = await asyncio.open_connection(url, 80)

    try:
        # Записать http-запрос и опустошить буфер писателя
        stream_writer.write(request.encode())
        await  stream_writer.drain()

        # Читать строки и сохранять их в списке
        responses = [response async for response in read_until_empty(stream_reader)]

        print(''.join(responses))
    finally:
        # Закрыть писатель и ждать завершения закрытия
        stream_writer.close()
        await stream_writer.wait_closed()


asyncio.run(main())
