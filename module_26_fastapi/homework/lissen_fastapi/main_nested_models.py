from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []


class ItemWithListStr(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Это приведёт к тому, что объект tags преобразуется в список, несмотря на то что тип его элементов не объявлен.

    """
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: ItemWithListStr):
    """
    Таким образом, в нашем примере мы можем явно указать тип данных для поля
    tags для ItemWithListStr как "список строк"
    """
    results = {"item_id": item_id, "item": item}
    return results
