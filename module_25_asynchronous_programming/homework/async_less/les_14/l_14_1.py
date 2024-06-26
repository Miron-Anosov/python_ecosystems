# Листинг 14.1 Класс исполнителя задач

import asyncio


class TaskRunner:

    def __init__(self):
        self.loop = asyncio.new_event_loop()  # при инициализации создаем новый собитийный цикл
        self.tasks = []  # создаем предварительный список всех задач, которые необходимо будет обработать.

    def add_task(self, func):
        self.tasks.append(func)

    async def _run_all(self):
        """Добавляем наши задачи в список ожидаемых задач и выполняем их инициализацию"""
        awaitable_tasks = []

        for task in self.tasks:
            if asyncio.iscoroutinefunction(task):
                awaitable_tasks.append(asyncio.create_task(task()))
            elif asyncio.iscoroutine(task):
                awaitable_tasks.append(asyncio.create_task(task))
            else:
                self.loop.call_soon(task)

        await asyncio.gather(*awaitable_tasks)

    def run(self):
        self.loop.run_until_complete(self._run_all())  # Запускается цикл событий


if __name__ == "__main__":
    def regular_function():
        print('Привет от регулярной функции!')


    async def coroutine_function():
        print('Выполняется сопрограмма, засыпаю!')
        await asyncio.sleep(1)
        print('Проснулась!')


    runner = TaskRunner()
    runner.add_task(coroutine_function)  # добавляем сопрограмму
    runner.add_task(coroutine_function())  # добавляем корутину
    runner.add_task(regular_function)  # добавляем обычную функцию
    runner.run()

"""
Исполнитель задач создает цикл событий и пустой список задач. Метод `add` добавляет функцию (или сопрограмму) в список 
ожидающих задач. Когда пользователь вызывает метод `run()`, мы выполняем метод `_run_all` в цикле событий. Этот метод 
перебирает задачи в списке и проверяет, является ли объект обычной функцией или сопрограммой. Если это сопрограмма, то 
мы создаем задачу, иначе вызываем метод цикла событий `call_soon`, чтобы запланировать выполнение функции на следующей 
итерации. Создав все задачи, мы должны вызвать для них сопрограмму `gather` и дождаться завершения.
Далее определяются две функции: обычная функция Python `regular_function` и сопрограмма `coroutine_function`. 
Мы создаем экземпляр `TaskRunner` и добавляем три задачи, вызывая `coroutine_function` дважды, чтобы продемонстрировать 
два разных способа сослаться на сопрограмму в нашем API.
"""
