from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Эта дополнительная информация будет включена в JSON Schema
    выходных данных для этой модели, и она будет использоваться в документации к API."""
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Pydantic schema_extra
    Вы можете объявить ключ example для модели Pydantic, используя класс Config и переменную
    schema_extra, как описано в Pydantic документации.
    """
    results = {"item_id": item_id, "item": item}
    return results
