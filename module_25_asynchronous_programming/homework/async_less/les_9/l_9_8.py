from typing import List, Dict

import asyncpg
from asyncpg import Pool
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route


async def create_database_pool():
    pool: Pool = await asyncpg.create_pool(host='127.0.0.1',
                                           port=5432,
                                           user='postgres',
                                           database='tester',
                                           password='postgres',
                                           min_size=6,
                                           max_size=32)
    app.state.DB = pool


async def destroy_database_pool():
    pool: Pool = app.state.DB
    await pool.close()


async def brands(request: Request) -> Response:
    connection: Pool = request.app.state.DB
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(brand) for brand in results]
    return JSONResponse(result_as_dict)


async def hello_world(request: Request) -> Response:
    response = {'message': 'Hello world'}
    print(request)
    return JSONResponse(response)


brands_route = Route('/brands', brands)
hw_route = Route('/', hello_world)


app = Starlette(routes=[brands_route, hw_route], on_startup=[create_database_pool], on_shutdown=[destroy_database_pool])


# uvicorn --workers 1 --log-level error l_9_8:app
