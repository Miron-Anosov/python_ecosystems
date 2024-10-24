from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


###################################################################


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


"""
Здесь, если запросить /unicorns/yolo, то операция пути вызовет UnicornException.
Но оно будет обработано unicorn_exception_handler.
Таким образом, вы получите чистую ошибку с кодом состояния HTTP 418 и содержимым JSON:
{"message": "Oops! yolo did something. There goes a rainbow..."}
"""

#############################################################################################


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc.status_code)
    print('StarletteHTTPException: обрабатывает HTTP-исключения, включая HTTPException')
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print('RequestValidationError: обрабатывает ошибки валидации запроса.')
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


"""
Переопределение исключений проверки запроса
Когда запрос содержит недопустимые данные, FastAPI внутренне вызывает ошибку RequestValidationError.
А также включает в себя обработчик исключений по умолчанию.
Чтобы переопределить его, импортируйте RequestValidationError и используйте его с 
@app.exception_handler(RequestValidationError) для создания обработчика исключений.
Обработчик исключения получит объект Request и исключение.
"""