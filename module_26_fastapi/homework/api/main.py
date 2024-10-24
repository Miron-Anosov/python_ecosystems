import uvicorn
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI

try:
    # TODO для выполнения тестов не получалось организовать импорт так что бы не возникала ошибка.
    from .core import router as recipes, engine, BaseORM
except ImportError:
    from core import router as recipes, engine, BaseORM


SUMMARY = "Это API для управления рецептами. Оно позволяет получать, создавать и обновлять рецепты."
DESCRIPTION = (Path(__file__).parent / 'static/description.md').read_text()

tags_metadata = [
    {
        "name": "Recipes",
        "description": "Попробуй это.",
    },
]

CONTACT = {
    "name": "Miron",
    "url": "http://x-force.example.com/contact/",
    "email": "miron-nicolaevich@gmail.com",
}

SERVERS = [
    {
        "url": "http://127.0.0.1:8000"
    }
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.async_engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
    yield
    async with engine.async_engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await engine.async_engine.dispose()


app = FastAPI(lifespan=lifespan, title="Menu", version="0.0.1.alfa",
              summary=SUMMARY,
              description=DESCRIPTION,
              contact=CONTACT,
              servers=SERVERS,
              openapi_tags=tags_metadata)

app.include_router(
    prefix='/v1/recipes',
    tags=['Recipes'],
    router=recipes)

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
