import asyncpg
from aiohttp import web
from aiohttp.web_response import Response
from aiohttp.web_request import Request
from aiohttp.web_app import Application
from asyncpg.types import Record
from asyncpg import Pool
from typing import List, Dict

routes = web.RouteTableDef()
DB_KEY = 'database'


async def create_database_pool(app_: Application):
    print('Создание пула подключений к БД')
    pool: Pool = await asyncpg.create_pool(host='127.0.0.1',
                                           port=5432,
                                           user='postgres',
                                           database='tester',
                                           password='postgres',
                                           min_size=6,
                                           max_size=32)
    app_[DB_KEY] = pool


async def destroy_database_pool(app_: Application):
    print('Закрытие пула подключений к БД')
    pool: Pool = app_.get(DB_KEY)
    await pool.close()


@routes.get('/brands')
async def brands(request: Request) -> Response:
    connection: Pool = request.app.get(DB_KEY)
    brands_query = "SELECT brand_id, brand_name FROM brand"
    results: List[Record] = await connection.fetch(brands_query)
    result_as_dict: List[Dict] = [dict(brand) for brand in results]
    return web.json_response(result_as_dict)


app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)
app.add_routes(routes)
web.run_app(app)
