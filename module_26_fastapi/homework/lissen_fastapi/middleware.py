import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
"""
Создайте промежуточное ПО
Для создания промежуточного программного обеспечения вы используете декоратор @app.middleware("http") поверх функции.
Функция промежуточного программного обеспечения получает:
    The request.
    Функция call_next который получит request в качестве параметра.
        Эта функция будет передавать request к соответствующей операции пути .
        Затем он возвращает response генерируется соответствующей операцией пут
"""