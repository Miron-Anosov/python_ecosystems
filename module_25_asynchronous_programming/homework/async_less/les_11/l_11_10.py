import asyncio
import functools
from asyncio import Event


def trigger_event(event: Event):
    event.set()


async def do_work_on_event(event: Event):
    print('Waiting for event...')
    await event.wait() #A
    print('Performing work!')
    await asyncio.sleep(1) #B
    print('Finished work!')
    event.clear() #C


async def main():
    event = asyncio.Event()
    asyncio.get_running_loop().call_later(5.0, functools.partial(trigger_event, event)) #D
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))


asyncio.run(main())

"""
Здесь мы написали сопрограмму `do_work_on_event`, которая принимает событие и первым делом вызывает его метод `wait`. 
Это действие блокирует выполнение, пока кто-то не вызовет метод события `set`, означающий, что событие произошло. 
Мы также написали простую функцию `trigger_event`, которая устанавливает данное событие. 

В сопрограмме `main` мы создаем объект события и вызываем метод `call_later`, который активирует его через 5 секунд. 
Затем мы дважды вызываем `do_work_on_event` с помощью `gather`, что создает две конкурентных задачи. Запустив программу,
мы увидим, что в течение 5 секунд задачи ничего не делают, ожидая события, а потом начинают работать.
"""