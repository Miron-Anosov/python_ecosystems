# Листинг 12.2 Использование методов-сопрограмм очереди
import asyncio
from asyncio import Queue
from random import randrange


class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id, products):
        self.customer_id = customer_id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    while True:
        """Используем блокирующий метод очереди, но в контексте асинхронного программирования он не блокирует всю
         программу, а только приостанавливает выполнение конкретной сопрограммы до получения элемента из очереди."""
        customer: Customer = await queue.get()
        print(f'Кассир {cashier_number} '
              f'обслуживает покупателя '
              f'{customer.customer_id}')
        for product in customer.products:
            print(f"Кассир {cashier_number} "
                  f"обслуживает покупателя "
                  f"{customer.customer_id}'s {product.name}")
            await asyncio.sleep(product.checkout_time)
        print(f'Кассир {cashier_number} '
              f'закончил обслуживать покупателя '
              f'{customer.customer_id}')
        queue.task_done()  # Оповещаем очередь о выпаленной задачи


def generate_customer(customer_id: int) -> Customer:
    """Сгенерировать случайного покупателя"""
    all_products = [Product('пиво', 2),
                    Product('бананы', .5),
                    Product('колбаса', .2),
                    Product('подгузники', .2)]
    products = [all_products[randrange(len(all_products))]
                for _ in range(randrange(10))]
    return Customer(customer_id, products)


async def customer_generator(queue: Queue):
    """Генерировать несколько случайных покупателей в секунду"""
    customer_count = 0

    while True:
        customers = [generate_customer(i)
                     for i in range(customer_count, customer_count + randrange(5))]
        for customer in customers:
            print('Ожидаю возможности поставить покупателя в очередь...')
            """используем блокирующий метод добавления в очередь, как и с get(), 
            этот метод является блокирующим в контексте асинхронного выполнения."""
            await queue.put(customer)
            print('Покупатель поставлен в очередь!')
        customer_count = customer_count + len(customers)  # Возрастающая очередь
        await asyncio.sleep(1)


async def main():
    customer_queue = Queue(5)
    # создаем задачу с бесконечным циклом и генерируем новых покупателей
    customer_producer = asyncio.create_task(customer_generator(customer_queue))

    cashiers = [asyncio.create_task(checkout_customer(customer_queue, i))
                for i in range(3)]  # Создаем трёх исполнителей.

    await asyncio.gather(customer_producer, *cashiers)


asyncio.run(main())


"""
Здесь сопрограмма `generate_customer` создает покупателя со случайным списком товаров. Сопрограмма `customer_generator` 
каждую секунду генерирует от одного до пяти случайных покупателей и добавляет их в очередь методом `put`.
 Поскольку `put` — это сопрограмма, при заполнении очереди `customer_generator` заблокирует выполнение до появления 
 свободного места. Если в очереди пять покупателей и производитель пытается добавить шестого, очередь заблокируется, 
 пока кассир не обслужит какого-то покупателя. Сопрограмму `customer_generator` можно считать производителем, поскольку 
 она порождает покупателей, обслуживаемых кассирами.

Мы также хотим, чтобы сопрограмма `checkout_customer` работала бесконечно, поскольку кассиры остаются на своих местах, 
даже когда очередь пуста. Поэтому `checkout_customer` вызывает метод-сопрограмму очереди `get`, который блокирует 
выполнение, если в очереди нет покупателей. В сопрограмме `main` мы создаем очередь на пять покупателей и три 
конкурентные задачи `checkout_customer`. Кассиров можно рассматривать как потребителей: они потребляют покупателей 
из очереди и обслуживают их.

Этот код случайным образом генерирует покупателей, но в какой-то момент очередь должна заполниться, потому что кассиры 
обслуживают покупателей не так быстро, как производитель их создает. Поэтому мы увидим картину, когда производитель 
приостанавливает добавление покупателей в очередь, пока какой-то покупатель не будет обслужен.
"""