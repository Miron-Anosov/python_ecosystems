import asyncpg
from asyncpg import Pool
from aiohttp import web
from aiohttp.web import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response


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


@routes.post('/product')
async def create_product(request: Request) -> Response:
    PRODUCT_NAME = 'product_name'
    BRAND_ID = 'brand_id'

    if not request.can_read_body:
        raise web.HTTPBadRequest()

    body = await request.json()

    if PRODUCT_NAME in body and BRAND_ID in body:
        db = request.app[DB_KEY]
        await db.execute('''INSERT INTO product(product_id, 
                                                product_name, 
                                                brand_id) 
                                                VALUES(DEFAULT, $1, $2)''',
                         body[PRODUCT_NAME],
                         int(body[BRAND_ID]))
        return web.Response(status=201)
    else:
        raise web.HTTPBadRequest()


app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app)


# curl -i -X POST -H "Content-Type: application/json" -d '{"product_name":"product_name", "brand_id":1}' http://localhost:8080/product
