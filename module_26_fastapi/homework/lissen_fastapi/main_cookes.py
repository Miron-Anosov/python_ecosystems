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

