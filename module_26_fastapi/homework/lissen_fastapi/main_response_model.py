# Response Model - Return Type

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
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


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    """
    Мы указали в response_model модель UserOut, в которой отсутствует поле,
    содержащее пароль - и он будет исключен из ответа
    """
    return user


"""
В нашем примере модели входных данных и выходных данных различаются. И если мы укажем аннотацию типа выходного значения 
функции как UserOut - проверка типов выдаст ошибку из-за того, что мы возвращаем некорректный тип. 
Поскольку это 2 разных класса.
Поэтому в нашем примере мы можем объявить тип ответа только в параметре response_model.
"""


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInput(BaseUser):
    password: str


@app.post("/user2/")
async def create_user(user: UserInput) -> BaseUser:
    """FastApi поймет что нужно вернуть BaseUser, хотя явно мы передаем UserIn. Тем самым мы не передадим пароль.
    В случе, если пыпытаемся отдавать модель без наследования, будет нарушена типизация"""
    return user


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


class ItemModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=ItemModel, response_model_exclude_unset=True)
async def read_item(item_id: str):
    """
    tags: List[str] = [], где пустой список [] является значением по умолчанию.
    но вы, возможно, хотели бы исключить их из ответа,
    если данные поля не были заданы явно."""
    return items[item_id]
