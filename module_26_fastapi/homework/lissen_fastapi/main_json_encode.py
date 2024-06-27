from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    items[item_id] = update_item_encoded
    return update_item_encoded

"""
Это означает, что если вы хотите обновить элемент bar, используя PUT с телом, содержащим:
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
поскольку оно не включает уже сохраненный атрибут "tax": 20.2, входная модель примет значение по умолчанию "tax": 10.5.
И данные будут сохранены с этим "новым" tax, равным 10,5.
"""
