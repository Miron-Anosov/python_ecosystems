import asyncio
import asyncpg

product_query = \
    """
SELECT
p.product_id,
p.product_name,
p.brand_id,
s.sku_id,
pc.product_color_name,
ps.product_size_name
FROM product as p
JOIN sku as s on s.product_id = p.product_id
JOIN product_color as pc on pc.product_color_id = s.product_color_id
JOIN product_size as ps on ps.product_size_id = s.product_size_id
WHERE p.product_id = 100"""


async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


async def main():
    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5432,
                                   user='postgres',
                                   database='tester',
                                   password='postgres',
                                   min_size=6,
                                   max_size=6) as pool:  # A

        await asyncio.gather(query_product(pool),
                             query_product(pool))  # B


asyncio.run(main())

"""
Здесь мы сначала создаем пул с шестью подключениями. Затем создается два объекта сопрограмм выполнения запросов,
конкурентная работа которых планируется с помощью asyncio.gather. Сопрограмма query_product сначала захватывает
подключение из пула, вызывая метод pool.acquire(). Затем она приостанавливается, до тех пор пока не освободится 
подключение. Это делается в блоке async with; тем самым гарантируется, что по выходе из блока подключение будет 
возвращено в пул. Это важно, потому что в противном случае подключения быстро закончились бы и приложение зависло бы в 
ожидании подключения, которого никогда не получит. 
Захватив подключение, мы можем выполнить запрос, как в предыдущих примерах.
"""