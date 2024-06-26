import asyncio
from asyncio import Task
import aiohttp
from aiohttp import web, ClientSession
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import logging
from typing import Dict, Set, Awaitable, Optional, List

routes = web.RouteTableDef()

PRODUCT_BASE = 'http://127.0.0.1:8000'
INVENTORY_BASE = 'http://127.0.0.1:8001'
FAVORITE_BASE = 'http://127.0.0.1:8002'
CART_BASE = 'http://127.0.0.1:8003'


@routes.get('/products/all')
async def all_products(request: Request) -> Response:
    async with aiohttp.ClientSession() as session:

        products = asyncio.create_task(session.get(f'{PRODUCT_BASE}/products'))
        favorites = asyncio.create_task(session.get(f'{FAVORITE_BASE}/users/3/favorites'))
        cart = asyncio.create_task(session.get(f'{CART_BASE}/users/3/cart'))

        requests = [products, favorites, cart]
        # Создать задачи всех 3-х сервисов и запустить их конкурентно
        done, pending = await asyncio.wait(requests, timeout=1.0)

        if products in pending:  # Если задача не была выполнена за отведенное время, отменить ее и вернуть 504 ошибку.
            [request.cancel() for request in requests]

            return web.json_response({'error': 'Could not reach products service.'}, status=504)

        elif products in done and products.exception() is not None:
            # Если задача была выполнена с ошибкой, отменить ее и вернуть 500 ошибку.
            [request.cancel() for request in requests]
            logging.exception('Server error reaching product service.', exc_info=products.exception())

            return web.json_response({'error': 'Server error reaching products service.'}, status=500)

        else:
            # Извлечь данные о товарах и переиспользовать их для получения данных об наличии.
            product_response = await products.result().json()
            product_results: List[Dict] = await get_products_with_inventory(session, product_response)

            cart_item_count: Optional[int] = await get_response_item_count(cart,
                                                                           done,
                                                                           pending,
                                                                           'Error getting user cart.')
            favorite_item_count: Optional[int] = await get_response_item_count(favorites,
                                                                               done,
                                                                               pending,
                                                                               'Error getting user favorites.')

            return web.json_response({'cart_items': cart_item_count,
                                      'favorite_items': favorite_item_count,
                                      'products': product_results})


async def get_products_with_inventory(session: ClientSession, product_response) -> List[Dict]:
    """Получить данные о товарах и запросить их наличие"""

    def get_inventory(session: ClientSession, product_id: str) -> Task:
        url = f"{INVENTORY_BASE}/products/{product_id}/inventory"
        return asyncio.create_task(session.get(url))

    def create_product_record(product_id: int, inventory: Optional[int]) -> Dict:
        return {'product_id': product_id, 'inventory': inventory}

    inventory_tasks_to_product_id = {
        get_inventory(session, product['product_id']): product['product_id'] for product in product_response
    }

    inventory_done, inventory_pending = await asyncio.wait(inventory_tasks_to_product_id.keys(), timeout=1.0)

    product_results = []

    for done_task in inventory_done:
        if done_task.exception() is None:
            product_id = inventory_tasks_to_product_id[done_task]
            inventory = await done_task.result().json()
            product_results.append(create_product_record(product_id, inventory['inventory']))
        else:
            # обрабатываем запросы с ошибками (результатом будет inventory=None)
            product_id = inventory_tasks_to_product_id[done_task]
            product_results.append(create_product_record(product_id, None))
            logging.exception(f'Error getting inventory for id {product_id}',
                              exc_info=inventory_tasks_to_product_id[done_task].exception())

    # Отменяем запросы, которые не выполнились и так же добавляем в список результатов
    for pending_task in inventory_pending:
        pending_task.cancel()
        product_id = inventory_tasks_to_product_id[pending_task]
        product_results.append(create_product_record(product_id, None))

    return product_results


async def get_response_item_count(task: Task,
                                  done: Set[Awaitable],
                                  pending: Set[Awaitable],
                                  error_msg: str) -> Optional[int]:
    if task in done and task.exception() is None:
        return len(await task.result().json())
    elif task in pending:
        task.cancel()
    else:
        logging.exception(error_msg, exc_info=task.exception())

    return None


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=9000)


"""
Здесь мы сначала определяем обработчик оконечной точки all_products. В нем мы с помощью функции wait конкурентно
 отправляем запросы о товарах, корзине и избранном, давая на завершение 1 с. Как только все они завершатся или 
 произойдет тайм-аут, мы начинаем обрабатывать результаты. Поскольку время получения ответа о товарах критично, мы 
 сначала проверяем состояние этого запроса. Если он еще выполняется или произошло исключение, то остальные запросы 
 снимаются, а клиенту возвращается сообщение об ошибке. Если было исключение, то мы возвращаем код HTTP 500 — ошибка 
 сервера. А в случае тайм-аута возвращаем код 504 — не удалось подключиться к сервису. Это различие оставляет клиенту 
 возможность решить, стоит ли пробовать еще раз, а также дает больше информации для мониторинга и оповещения 
 (например, можно завести извещатели, следящие за частотой ответов с кодом 504).

Если от сервиса товаров получен успешный ответ, то можно начать его обработку и запросить складские остатки. 
Это делается в функции get_products_with_inventory. Мы извлекаем идентификаторы товаров из тела ответа и на их основе 
конструируем запросы к сервису наличия на складе. Поскольку этот сервис принимает один идентификатор в одном запросе 
(в идеале хорошо бы объединить все идентификаторы в пакет, но будем считать, что команда, разрабатывающая сервис 
наличия, столкнулась с проблемами при реализации такого подхода), мы создадим список задач для запроса сведений о 
наличии каждого товара. И снова передадим их сопрограмме wait, дав 1 с на завершение.

Поскольку сведения о наличии на складе факультативны, по истечении тайм-аута мы начинаем обрабатывать множества done и 
pending. Если от сервиса наличия на складе получен успешный ответ, то мы создаем словарь, содержащий информацию 
о товаре, дополненную остатком на складе. Если имело место исключение или запрос все еще находится в множестве pending, 
то в записи словаря вместо остатка будет фигурировать значение None, означающее, что мы не смогли получить данные. 
На этапе преобразования ответ в формате JSON None будет заменено на null.

Наконец, мы проверяем ответы от сервисов корзины и избранного. От них нам нужно только одно число. Поскольку логика 
почти идентична, мы написали вспомогательную функцию подсчета элементов в ответе, get_response_item_count. 
Если сервис корзины или избранного завершился успешно, то мы получим JSON-массив, поэтому подсчитываем и возвращаем 
число элементов в нем. Если же произошло исключение или тайм-аут, то мы возвращаем результат None, который 
преобразуется в null в JSON-ответе.
"""