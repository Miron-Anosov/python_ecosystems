import asyncio
import asyncpg
from asyncpg.transaction import Transaction


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='tester',
                                       password='postgres')
    transaction: Transaction = connection.transaction()  # A
    await transaction.start()  # B
    try:
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Errors, rolling back transaction!')
        await transaction.rollback()  # C
    else:
        print('No errors, committing transaction!')
        await transaction.commit()  # D

    query = """SELECT brand_name FROM brand 
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()


asyncio.run(main())

"""
Мы начинаем с того, что создаем транзакцию тем же методом, который использовали при работе с асинхронным контекстным
менеджером, но теперь сохраняем возвращенный экземпляр класса Transaction. Этот класс можно рассматривать как менеджер 
нашей транзакции, поскольку он умеет фиксировать и откатывать транзакцию по мере необходимости. 
Имея экземпляр транзакции, мы вызываем сопрограмму start. Она выполняет запрос к Postgres, необходимый, чтобы начать 
транзакцию. Затем в блоке try можем выполнять произвольные запросы. В данном случае мы вставляем две марки. Если хотя 
бы одна команда INSERT завершится ошибкой, то мы попадем в блок except и откатим транзакцию, 
вызвав сопрограмму rollback. Если же ошибок не было, то вызываем сопрограмму commit, которая завершает транзакцию 
и делает все изменения в базе данных постоянными.
"""
