import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')

    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)

    await connection.close()


asyncio.run(main())


"""
Здесь распечатываются все имеющиеся товары. Хотя в таблице хранится 1000 товаров, в память загружается лишь небольшая
порция. На момент написания книги объем предвыборки по умолчанию был равен 50 записей, чтобы уменьшить затраты на 
сетевой трафик. Это значение можно изменить, задав параметр prefetch.
"""