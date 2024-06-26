import asyncio


@asyncio.coroutines
def coroutine_():
    print('Sleeping!')
    yield from asyncio.sleep(1)
    print('Finished!')


asyncio.run(coroutine_())

"""
Вместо ключевого слова `async` мы применили декоратор `@asyncio.coroutine`, который указывает, что функция является 
сопрограммой. А вместо ключевого слова `await` используется конструкция `yield from`, знакомая по использованию 
генераторов. В современных версиях ключевые слова `async` и `await` — это не более чем синтаксический сахар, 
обертывающий эту конструкцию. В Python 3.10 был удалён устаревший синтаксис с декоратором @asyncio.coroutine и старым 
способом определения корутин через yield from в пользу синтаксиса с использованием async def и await.
"""