from enum import Enum
from typing import Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()


class Tags(Enum):
    items = "items"
    users = "users"


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED,
          summary="Create an item.",
          description="Create an item with all the information, name, description, price, tax and a set of unique tags",
          deprecated=True
          )
async def create_item(item: Item):
    return item


@app.post("/items2/", response_model=Item, tags=[Tags.items], response_description="The created item..")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get("/items/", tags=[Tags.users])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
