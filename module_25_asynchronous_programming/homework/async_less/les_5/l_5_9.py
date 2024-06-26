import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')
    async with connection.transaction():  # Начало транзакции
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')")

    query = """SELECT brand_name FROM brand 
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)  # Проверяем
    print(brands)

    await connection.close()


asyncio.run(main())
