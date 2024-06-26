import asyncio
import asyncpg
from asyncpg import Record
from typing import List


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')

    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    query = "SELECT * FROM brand"
    result: List[Record] = await connection.fetch(query)

    for brand in result:
        print(f'{brand["brand_id"]=}, {brand["brand_name"]=}')


if __name__ == '__main__':
    asyncio.run(main())
