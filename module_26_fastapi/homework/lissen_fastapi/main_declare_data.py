from fastapi import FastAPI
from pydantic import BaseModel, Field

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


class ItemTwo(BaseModel):
    """
    Дополнительные аргументы поля Field
    При использовании Field() с моделями Pydantic, вы также можете объявлять дополнительную информацию
    для JSON Schema, передавая любые другие произвольные аргументы в функцию.
    Вы можете использовать это, чтобы добавить аргумент example для каждого поля.
    Имейте в виду, что эти дополнительные переданные аргументы не добавляют никакой валидации,
    только дополнительную информацию для документации.
    """

    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Pydantic schema_extra
    Вы можете объявить ключ example для модели Pydantic, используя класс Config и переменную
    schema_extra, как описано в Pydantic документации.
    """
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: ItemTwo):
    """Использование Field(examples=[<any>])"""
    results = {"item_id": item_id, "item": item}
    return results
