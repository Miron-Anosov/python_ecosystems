# https://fastapi.tiangolo.com/ru/tutorial/cookie-params/
from typing import Annotated

from fastapi import Cookie, FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    """
    Для объявления cookies, вам нужно использовать Cookie,
    иначе параметры будут интерпретированы как параметры запроса.
            {
          "ads_id": null
        }
    curl -b "ads_id=12345" http://localhost:8000/items/

    """
    print(f'{ads_id=}')
    return {"ads_id": ads_id}


@app.get("/header/")
async def read_header(user_agent: Annotated[str | None, Header()] = None):
    """
    Чтобы объявить заголовки, важно использовать Header, иначе параметры интерпретируются как query-параметры.
    По умолчанию Header преобразует символы имен параметров из символа подчеркивания (_) в дефис (-) для извлечения
    и документирования заголовков.
    """
    print('user_agent', user_agent)
    return {"User-Agent": user_agent}


@app.get("/header2/")
async def read_list_headers(x_token: Annotated[list[str] | None, Header()] = None):
    """
    Вы получите все значения из повторяющегося заголовка в виде list Python.
    Например, чтобы объявить заголовок X-Token, который может появляться более одного раза.
    Returns:
        {
        "X-Token values": [
            "bar",
            "foo"
        ]
    }
    """
    return {"X-Token values": x_token}

