import asyncio
import asyncpg
import logging


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")

        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as ex:
            logging.warning('Ignoring error inserting product color', exc_info=ex)

    await connection.close()


asyncio.run(main())

"""
Здесь первая команда INSERT выполнена успешно, потому что такой марки в базе еще нет. А при выполнении второй команды
INSERT возникает ошибка дубликата ключа. Поскольку вторая команда находится внутри транзакции и мы перехватили и 
запротоколировали исключение, то, несмотря на ошибку, внешняя транзакция не откатывается и новая марка 
вставляется в базу. Не будь вложенной транзакции, ошибка во второй команде вставки привела бы к откату вставки марки.

WARNING:root:Ignoring error inserting product color
Traceback (most recent call last):
  File "/home/miron/PycharmProjects/python_advanced/module_25_asynchronous_programming/homework/async_less/les_5/l_5_11.py", line 17, in main
    await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
  File "/home/miron/PycharmProjects/python_advanced/.venv/lib/python3.12/site-packages/asyncpg/connection.py", line 350, in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg/protocol/protocol.pyx", line 374, in query
asyncpg.exceptions.UniqueViolationError: duplicate key value violates unique constraint "product_color_pkey"
DETAIL:  Key (product_color_id)=(1) already exists.

"""