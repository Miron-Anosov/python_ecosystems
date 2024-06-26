import asyncpg
import asyncio


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'
        cursor = await connection.cursor(query)
        await cursor.forward(500)
        products = await cursor.fetch(100)
        for product in products:
            print(product)

    await connection.close()


asyncio.run(main())

"""
Здесь мы сначала создаем курсор для запроса. Обратите внимание, что это делается в предложении await, как для 
сопрограммы, а не асинхронного генератора; это возможно, потому что в asyncpg курсор является одновременно асинхронным 
генератором и объектом, допускающим ожидание. В большинстве случаев оба способа похожи, но при таком создании курсора 
есть различия в поведении предвыборки – мы не можем задать количество выбираемых за одно обращение записей; попытка 
сделать это приведет к исключению InterfaceError. Получив курсор, мы вызываем его метод-сопрограмму forward, чтобы 
сдвинуться вперед по результирующему набору. В результате мы пропустим первые 500 записей в таблице товаров. Затем 
выбираем следующие 100 товаров и печатаем их на консоли.
"""