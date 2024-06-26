from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    """
    Вы можете объявлять дополнительную информацию в Field, Query, Body и т.п.
    Она будет включена в сгенерированную JSON схему.
    """
    results = {"item_id": item_id, "item": item}
    return results
