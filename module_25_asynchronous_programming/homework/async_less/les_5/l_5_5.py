import asyncio
import asyncpg
from random import sample
from typing import List, Tuple, Union


def load_common_words():
    with open('words.txt', mode='r') as file:
        return file.readlines()


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str,]]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brand(common_words, connection):
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand Values(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')

    await insert_brand(common_words, connection)


if __name__ == '__main__':
    asyncio.run(main())
