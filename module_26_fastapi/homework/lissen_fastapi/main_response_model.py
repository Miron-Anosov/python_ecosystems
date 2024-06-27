# Response Model - Return Type

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from typing import Any

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class UserIn(BaseModel):
    """
    Получить и вернуть один и тот же тип данных
    Здесь мы объявили модель UserIn, которая хранит пользовательский пароль в открытом виде
    """
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


"""
Валидации ответа.
Если данные невалидны (например, отсутствует одно из полей), это означает, что код вашего приложения работает 
некорректно и функция возвращает не то, что вы ожидаете. В таком случае приложение вернет server error вместо 
того, чтобы отправить неправильные данные. Таким образом, вы и ваши пользователи можете быть уверены, что получите 
корректные данные в том виде, в котором они ожидаются.
Но самое важное:
Ответ будет ограничен и отфильтрован - т.е. в нем останутся только те данные, которые определены в возвращаемом типе.
"""


@app.post("/items3/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items4/", response_model=list[Item])
async def read_items() -> Any:
    """
    response_model принимает те же типы, которые можно указать для какого-либо поля в модели Pydantic.
    Таким образом, это может быть как одиночная модель Pydantic, так и список (list) моделей Pydantic.
    Например, List[Item].
    """
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
