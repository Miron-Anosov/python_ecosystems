from typing import Annotated, Union

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(
        item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: Union[str, None] = None,
        item: Union[Item, None] = None,
):
    """
    Во-первых, конечно, вы можете объединять параметры Path, Query и объявления тела запроса в своих функциях обработки,
     FastAPI автоматически определит, что с ними нужно делать.

    Вы также можете объявить параметры тела запроса как необязательные, установив значение по умолчанию, равное None:
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    """Обратите внимание, что хотя параметр item был объявлен таким же способом, как и раньше, теперь предполагается,
    что он находится внутри тела с ключом item."""
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.put("/items3/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item,
        user: User,
        importance: Annotated[int, Body(gt=0)],
        q: str | None = None,
):
    """
    Множество body и query параметров

    Конечно, вы также можете объявлять query-параметры в любое время, дополнительно к любым body-параметрам.
    Поскольку по умолчанию, отдельные значения интерпретируются как query-параметры, вам не нужно явно добавлять Query.

    Body также имеет все те же дополнительные параметры валидации и метаданных, как у Query, Path и других, которые
    вы увидите позже.
    """
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.put("/items4/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    """
    Добавление одного body-параметра¶
    Предположим, у вас есть только один body-параметр item из Pydantic модели Item.
    По умолчанию, FastAPI ожидает получить тело запроса напрямую.
    Но если вы хотите чтобы он ожидал JSON с ключом item с содержимым модели внутри, также как это происходит при
    объявлении дополнительных body-параметров, вы можете использовать специальный параметр embed у типа Body.
    С embed=True:
    Когда вы используете Body(embed=True), FastAPI ожидает, что JSON будет иметь дополнительный уровень вложенности,
    где данные модели Item находятся под ключом item
    """
    results = {"item_id": item_id, "item": item}
    return results


"""
Вы можете добавлять несколько body-параметров вашей функции операции пути, несмотря даже на то, что запрос может 
содержать только одно тело.
Но FastAPI справится с этим, предоставит правильные данные в вашей функции, а также сделает валидацию и документацию 
правильной схемы операции пути.
Вы также можете объявить отдельные значения для получения в рамках тела запроса.
И вы можете настроить FastAPI таким образом, чтобы включить тело запроса в ключ, даже если объявлен только один 
параметр.
"""


" http://127.0.0.1:8000/openapi.json"
" http://127.0.0.1:8000/docs"
" http://127.0.0.1:8000/redoc"
"uvicorn main:app --reload"
"fastapi dev main.py"
