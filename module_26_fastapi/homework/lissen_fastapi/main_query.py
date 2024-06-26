from typing import Union
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def main():
    return {'message': 'hello world'}


@app.get("/items/{item_id}")
async def get_item(item_id: int, q: str | None = None, short: bool = False):
    """Также обратите внимание, что FastAPI достаточно умён чтобы заметить,
    что параметр item_id является path-параметром, а q нет, поэтому, это параметр запроса."""
    item = {"item_id": item_id}
    if q:
        return {'item_id': item_id, 'q': q}
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an item"""
    return {'item_name': item.name, 'item_id': item_id}


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW'}
    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}
    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get('/files/{file_path:path}')
async def get_file(file_path: str):
    return {'file_path': file_path}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100):
    return fake_items_db[skip:skip + limit]


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int, q: str | None = None, shots: bool = False):
    items = {'item_id': item_id, 'user_id': user_id}
    if q:
        items.update({"q": q})
    if not shots:
        items.update({"description": "This is an amazing item that has a long description"})

    return items


@app.get("/items_required/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item



" http://127.0.0.1:8000/openapi.json"
" http://127.0.0.1:8000/docs"
" http://127.0.0.1:8000/redoc"
"uvicorn main:app --reload"
"fastapi dev main.py"
