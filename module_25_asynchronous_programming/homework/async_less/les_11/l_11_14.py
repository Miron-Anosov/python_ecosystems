import asyncio
from asyncio import Condition


async def do_work(condition: Condition):
    while True:
        print('Waiting for condition lock...')
        async with condition:  # Ждать возможности захватить блокировку условия, после захвата-освободить блокировку.
            print('Acquired lock, releasing and waiting for condition...')
            await condition.wait()  # Ждать события, когда оно произойдет, заново захватить блокировку условия.
            print('Condition event fired, re-acquiring lock and doing work...')
            await asyncio.sleep(1)
        print('Work finished, lock released.')
        # после выхода из блока, освободить блокировку словия.

async def fire_event(condition: Condition):
    while True:
        await asyncio.sleep(5)
        print('About to notify, acquiring condition lock...')
        async with condition:
            print('Lock acquired, notifying all workers.')
            condition.notify_all()  # Уведомить все задачи о событии.
        print('Notification finished, releasing lock.')


async def main():
    condition = Condition()

    asyncio.create_task(fire_event(condition))
    await asyncio.gather(do_work(condition), do_work(condition))


asyncio.run(main())
"""
Здесь у нас есть две сопрограммы: do_work и fire_event. Метод do_work захватывает условие, аналогично захвату 
блокировки, и затем вызывает метод wait условия. Этот метод блокирует выполнение, пока кто-то не вызовет метод 
notify_all условия.

Сопрограмма fire_event спит некоторое время, затем захватывает условие и вызывает метод notify_all, который пробуждает 
все задачи, ожидающие условия. В сопрограмме main мы создаем и конкурентно запускаем одну задачу fire_event 
и две задачи do_work.
"""