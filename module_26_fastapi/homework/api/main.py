import uvicorn
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from core import route as recipes, engine, BaseORM

SUMMARY = "Это API для управления рецептами. Оно позволяет получать, создавать и обновлять рецепты."
DESCRIPTION = (Path(__file__).parent / 'static/description.md').read_text()

tags_metadata = [
    {
        "name": "Recipes",
        "description": "Operations with recipes here .",
    },
]

CONTACT = {
    "name": "Miron",
    "url": "http://x-force.example.com/contact/",
    "email": "miron-nicolaevich@gmail.com",
}

SERVERS = [
    {
        "url": "http://localhost:8000/v1"
    }
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.async_engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
    yield
    async with engine.async_engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)


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
