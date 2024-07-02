import pytest
from httpx import AsyncClient, codes

from ..app.main import app

BASE_URL = "http://127.0.0.1:8000"
GET_ALL_RECIPES_URI_PREFIX = '/recipes'


@pytest.mark.anyio
async def test_get_all_recipes():

    async with AsyncClient(app=app, base_url=BASE_URL) as test_route:
        response = await test_route.get(GET_ALL_RECIPES_URI_PREFIX)
        assert response.status_code == codes.OK
