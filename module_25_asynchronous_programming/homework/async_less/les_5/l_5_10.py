import asyncio
import logging
import asyncpg


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)  # Корректные денные. Но не будут добавлены в БД.
            await connection.execute(insert_brand)  # Вызовет исключение
    except Exception:
        logging.exception('Error while running transaction')
    finally:
        query = """SELECT brand_name FROM brand 
                    WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)
        print(f'Query result was: {brands}')   # убеждаемся что транзакция не прошла

        await connection.close()


asyncio.run(main())

"""
Вторая команда возбудила исключение, и вот что мы увидим:
ERROR:root:Ошибка при выполнении транзакции
Traceback (most recent call last):
  File "listing_5_10.py", line 16, in main
    await connection.execute("INSERT INTO brand "
  File "asyncpg/connection.py", line 272, in execute
    return await self._protocol.query(query, timeout)
  File "asyncpg/protocol/protocol.pyx", line 316, in query
    asyncpg.exceptions.UniqueViolationError: duplicate key value violates unique constraint "brand_pkey"
DETAIL: Key (brand_id)=(9999) already exists.
Query result was: []
Сначала возникло исключение, потому что мы пытались вставить дубликат ключа, а  затем мы видим, что результат 
команды select пуст, т. е. мы успешно откатили транзакцию.
"""