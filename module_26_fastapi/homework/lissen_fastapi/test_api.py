from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    """
    Обратите внимание, что тестирующая функция является обычной def, а не асинхронной async def.
    И вызов клиента также осуществляется без await.
    Это позволяет вам использовать pytest без лишних усложнений.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

