# Попытка создать состояние гонки.
import asyncio

counter: int = 0


async def increment():
    global counter
    temp_counter = counter
    temp_counter = temp_counter + 1
    await asyncio.sleep(0.01)
    counter = temp_counter


async def main():
    global counter
    for _ in range(1000):
        tasks = [asyncio.create_task(increment()) for _ in range(100)]
        await asyncio.gather(*tasks)
        print(f'Counter is {counter}')
        assert counter == 100
        counter = 0


asyncio.run(main())

"""
Теперь сопрограмма `increment` не инкрементирует счётчик непосредственно, а сначала читает его во временную переменную, 
после чего прибавляет к этой переменной 1. Затем мы выполняем `await asyncio.sleep`, имитируя медленную операцию, 
которая приостанавливает нашу сопрограмму, и только потом записываем значение из временной переменной в глобальную 
переменную `counter`. Выполнив эту программу, вы увидите, что утверждение сразу же оказывается ложным и счётчик 
успевает добраться только до 1! Каждая сопрограмма сначала читает значение, равное 0, сохраняет его в переменной 
`temp`, а затем засыпает. Поскольку поток всего один, все операции чтения временной переменной выполняются 
последовательно, т. е. каждая сопрограмма сохраняет значение счётчика 0 и увеличивает его до 1. Затем, как только 
сон завершится, каждая сопрограмма записывает в счётчик значение 1, т. е. несмотря на то, что работает 100 сопрограмм, 
увеличивающих счётчик, новым его значением будет 1. Заметим, что если убрать выражение `await`, то порядок выполнения 
будет правильный, потому что исчезла возможность изменить состояние приложения, 
пока сопрограмма приостановлена в точке `await`.
"""