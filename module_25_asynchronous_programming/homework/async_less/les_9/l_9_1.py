# Листинг 9.1 Оконечная точка для возврата текущего времени
from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

route = web.RouteTableDef()


@route.get('/time')
async def time(request: Request) -> Response:
    """Создать оконечную GET-точку time; когда клиент обратится к ней, будет вызвана сопрограмма time"""
    today = datetime.today()
    result = {
        'month': today.month,
        'day': today.day,
        'time': str(today.time())
    }
    print(request.headers)
    return web.json_response(result)


app = web.Application()
app.add_routes(route)
web.run_app(app)
