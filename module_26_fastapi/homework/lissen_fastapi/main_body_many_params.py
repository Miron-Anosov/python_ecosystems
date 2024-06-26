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


" http://127.0.0.1:8000/openapi.json"
" http://127.0.0.1:8000/docs"
" http://127.0.0.1:8000/redoc"
"uvicorn main:app --reload"
"fastapi dev main.py"
