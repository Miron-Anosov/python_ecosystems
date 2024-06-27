from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """
    апример, в одном из способов использования спецификации OAuth2 (называемом "потоком пароля") требуется
    отправить username и password в виде полей формы.
    Данный способ требует отправку данных для авторизации посредством формы (а не JSON) и обязательного наличия
    в форме строго именованных полей username и password.
    Вы можете настроить Form точно так же, как настраиваете и Body ( Query, Path, Cookie), включая валидации,
    примеры, псевдонимы (например, user-name вместо username) и т.д.
    """
    return {"username": username}
