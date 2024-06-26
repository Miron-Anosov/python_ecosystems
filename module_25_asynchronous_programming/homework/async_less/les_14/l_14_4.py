import asyncio
from asyncio import StreamReader, StreamWriter
import uvloop


async def connected(reader: StreamReader, writer: StreamWriter):
    line = await reader.readline()
    writer.write(line)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(connected, port=9000)
    await server.serve_forever()


uvloop.install()  # Устанавливаем в качестве цикла событий uvloop
asyncio.run(main())

"""
Важно только, чтобы этот вызов был произведен раньше, чем вызов `asyncio.run(main())`. Под капотом `asyncio.run` 
вызывает функцию `get_event_loop`, которая создает цикл событий, если он еще не существует. Если сделать это до того, 
как `uvloop` был установлен, то мы получим стандартный цикл событий, 
и последующая установка `uvloop` уже ничего не изменит.
"""