# Листинг 11.13: Исполнители не успевают за событиями.
import asyncio
from asyncio import Event
from contextlib import suppress


async def trigger_event_periodically(event: Event):
    """Имитирует периодическое поступление новых задач"""
    while True:
        print('Triggering event!')
        event.set()
        await asyncio.sleep(1)


async def do_work_on_event(event: Event):
    while True:
        print('Waiting for event...')
        await event.wait()  # Ожидание события
        event.clear()  # После получения события, очищает его.
        print('Performing work!')
        await asyncio.sleep(5)
        print('Finished work!')


async def main():
    event = asyncio.Event()
    trigger = asyncio.wait_for(trigger_event_periodically(event), 5.0)

    with suppress(asyncio.TimeoutError):
        await asyncio.gather(do_work_on_event(event), do_work_on_event(event), trigger)


asyncio.run(main())

"""
При выполнении этой программы мы видим, что событие активируется, 
и оба исполнителя начинают работать параллельно. В это время мы продолжаем генерировать новые события. 
Поскольку исполнители заняты, они не обрабатывают второе событие до тех пор, пока не закончат текущую работу и не 
вызовут event.wait() второй раз. Если критично реагировать на каждое событие, необходимо использовать очередь.
"""
