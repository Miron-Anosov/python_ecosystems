from typing import Union, Annotated
from enum import Enum

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
        item_id: Annotated[int, Path(title="TITLE PATH", description="The ID of the item to get", ge=1, gt=5)],
        q: Annotated[str | None, Query(alias="item-query", title="Query string")] = None,
):
    """Поддержка Annotated была добавлена в FastAPI начиная с версии 0.95.0 (и с этой версии рекомендуется
    использовать этот подход).
    Если вы используете более старую версию, вы столкнётесь с ошибками при попытке использовать Annotated.
    Убедитесь, что вы обновили версию FastAPI как минимум до 0.95.1 перед тем, как использовать Annotated"""
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/integer-items/{item_id}/{x}")
async def read_items(
        item_id: Annotated[int, Path(ge=5, title="Items Int", description="greater-than-or-equal")],
        x: Annotated[int, Path(le=5, ge=15, title="Less than or equal")]
):
    """
    Валидация числовых данных: больше и меньше или равно

    То же самое применимо к:

        gt: больше (greater than)
        le: меньше или равно (less than or equal)
        ge: должен быть больше или равен ("greater than or equal")
    """
    results = {"item_id": item_id}

    if x:
        results.update({'x': x})
    return results



" http://127.0.0.1:8000/openapi.json"
" http://127.0.0.1:8000/docs"
" http://127.0.0.1:8000/redoc"
"uvicorn main:app --reload"
"fastapi dev main.py"
