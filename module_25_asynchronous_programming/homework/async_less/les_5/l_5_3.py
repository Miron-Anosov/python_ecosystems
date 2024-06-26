import asyncpg
import asyncio
from module_25_asynchronous_programming.homework.async_less.les_5.l_5_2 import *


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')
    statements = [CREATE_BRAND_TABLE,
                  CREATE_PRODUCT_TABLE,
                  CREATE_PRODUCT_COLOR_TABLE,
                  CREATE_PRODUCT_SIZE_TABLE,
                  CREATE_SKU_TABLE,
                  SIZE_INSERT,
                  COLOR_INSERT]

    print('Creating the product database...')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('Finished creating the product database!')
    await connection.close()


asyncio.run(main())

"""
В этом примере мы ожидаем завершения каждой SQL- команды с помощью await в цикле for,
поэтому команды INSERT будут выполнены синхронно. Поскольку одни таблицы зависят от других,
мы не можем выполнять эти команды конкурентно.
"""