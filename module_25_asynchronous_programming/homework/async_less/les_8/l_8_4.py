# Листинг 8.4 Попытка выполнения задач в фоновом режиме
import asyncio

from module_25_asynchronous_programming.homework.async_less.util import delay


async def main():
    while True:
        delay_time = input('Введите время сна:')
        asyncio.create_task(delay(int(delay_time)))


asyncio.run(main())

"""
На самом деле нам нужно, чтобы функция input была сопрограммой, чтобы можно было написать нечто вроде 
delay_time = await input('Введите время сна:'). Тогда наша задача была бы корректно запланирована и продолжала бы 
работать, пока мы ждем ввода данных пользователем. К сожалению, сопрограммного варианта input не существует, 
нужно придумать что-то другое.

Один из способов решения этой проблемы — выполнение блокирующего ввода в отдельном потоке и 
ожидание его завершения с помощью asyncio.
"""