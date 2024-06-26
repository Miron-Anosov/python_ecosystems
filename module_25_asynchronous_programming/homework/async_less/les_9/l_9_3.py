import aiohttp
import asyncpg
from aiohttp.web_response import Response
from aiohttp.web_request import Request
from aiohttp.web_app import Application
from aiohttp import web
from asyncpg import Record
from asyncpg import Pool

routes = web.RouteTableDef()

DB_KEY = 'database'


async def create_database_pool(app_: Application) -> None:
    pool: Pool = await asyncpg.create_pool(host='127.0.0.1',
                                           port=5432,
                                           user='postgres',
                                           database='tester',
                                           password='postgres',
                                           min_size=6,
                                           max_size=32)
    app_[DB_KEY] = pool


async def destroy_database_pool(app_: Application) -> None:
    pool = app_.get(DB_KEY)
    await pool.close()


@routes.get('/products/{id}')
async def get_product_by_id(request: Request) -> Response:
    try:
        str_id = request.match_info['id']  # извлекаем значение по ключу
        product_id = int(str_id)

        query = \
            """
            SELECT
            product_id,
            product_name,
            brand_id
            FROM product
            WHERE product_id = $1
            """
        connection: Pool = request.app.get(DB_KEY)
        result: Record = await connection.fetchrow(query, product_id)  # Выполняем запрос для одного товара
        if result is not None:
            return web.json_response(dict(result))
        else:

            raise web.HTTPNotFound()
    except ValueError as er:
        print(er)
        return web.HTTPBadRequest()


app = Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)
app.add_routes(routes)

web.run_app(app)
