# Листинг 12.3 Использование очередей в веб-приложении
import asyncio
from asyncio import Queue, Task
from typing import List
from random import randrange
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()

QUEUE_KEY = 'order_queue'
TASKS_KEY = 'order_tasks'


async def process_order_worker(worker_id: int, queue: Queue):
    """Выбрать заказ из очереди и обработать его"""
    while True:
        print(f'Исполнитель {worker_id}: ожидание заказа...')
        order = await queue.get()
        print(f'Исполнитель {worker_id}: обрабатывается заказ {order}')
        await asyncio.sleep(order)
        print(f'Исполнитель {worker_id}: заказ {order} обработан')
        queue.task_done()


@routes.post('/order')
async def place_order(request: Request) -> Response:
    """Поместить заказ в очередь и ответить пользователю немедленно"""
    order_queue = app[QUEUE_KEY]
    await order_queue.put(randrange(5))

    return Response(body='Order placed!')


async def create_order_queue(app: Application):
    """Создать очередь на 10 элементов и 5 задач-исполнителей"""
    print('Создание очереди заказов и задач.')
    queue: Queue = asyncio.Queue(10)
    app[QUEUE_KEY] = queue
    app[TASKS_KEY] = [asyncio.create_task(process_order_worker(i, queue))
                      for i in range(5)]


async def destroy_queue(app: Application):
    """Ждать завершения работающих задач"""
    order_tasks: List[Task] = app[TASKS_KEY]
    queue: Queue = app[QUEUE_KEY]
    print('Ожидание завершения исполнителей в очереди...')
    try:
        await asyncio.wait_for(queue.join(), timeout=10)
    finally:
        print('Обработка всех заказов завершена, отменяются задачи-исполнители...')
        [task.cancel() for task in order_tasks]


app = web.Application()
app.on_startup.append(create_order_queue)
app.on_shutdown.append(destroy_queue)

app.add_routes(routes)
web.run_app(app)

"""
Здесь первой идет сопрограмма `process_order_worker`. Она выбирает из очереди элемент — в данном случае целое число — и 
засыпает на это время, моделируя работу с медленной системой управления заказами. Эта сопрограмма крутится в бесконечном
цикле, выбирая из очереди и обрабатывая элементы.

Следующие сопрограммы, `create_order_queue` и `destroy_order_queue`, создают и уничтожают очередь. Создание не вызывает 
затруднений: мы просто инициализируем очередь asyncio на 10 элементов, после чего создаем пять задач-исполнителей и 
сохраняем их в экземпляре Application.

Уничтожение очереди чуть сложнее. Сначала с помощью `Queue.join` нужно дождаться, когда все находящиеся в очереди 
элементы будут обработаны. Поскольку в этот момент производится остановка приложения, новых HTTP-запросов не 
предвидится, то есть в очередь больше не будут помещаться заказы. Это означает, что все находящиеся в очереди заказы 
будут обработаны исполнителями. На всякий случай мы обернули вызов `join` методом `wait_for`, ограничив время ожидания 
10 секунд. Это разумно, так как мы не хотим, чтобы какая-нибудь сбойная задача помешала приложению остановиться.

Наконец, определяем маршрут для нашего приложения. Оконечная точка `/order` типа POST создает случайную задержку и 
помещает ее в очередь. Поместив такой «заказ» в очередь, мы возвращаем пользователю код состояния HTTP 200, 
сопровождаемый коротким сообщением. Отметим, что мы воспользовались сопрограммным вариантом `put`, то есть если очередь 
уже заполнена, то обработка запроса будет приостановлена, пока сообщение не попадет в очередь, что может занять 
некоторое время. Можно было бы вместо этого вызывать функцию `put_nowait` и возвращать код состояния HTTP 500 или 
какой-то другой код ошибки, предлагая пользователю повторить запрос позже. Мы решили, что можно немного подождать, 
пока запрос добавляется в очередь. Но если ваше приложение должно «отказывать быстро», то возвращать код ошибки при 
заполненной очереди, наверное, будет правильнее.

Очереди asyncio не предлагают готового решения для сохранения задач или обеспечения долговечности очереди. 
Если мы хотим защитить находящиеся в очереди задачи от подобных проблем, то должны добавить метод, сохраняющий их 
где-то, например, в базе данных. Но правильнее было бы использовать отдельную очередь вне asyncio, которая поддерживает 
долговременное хранение. Примерами сохраняемых на диске очередей задач являются Celery и RabbitMQ.
"""