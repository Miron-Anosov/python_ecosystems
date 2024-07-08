import pytest
from httpx import codes
import httpx
import pytest_asyncio

from asgi_lifespan import LifespanManager


from ..api.core.settings import settings

try:
    assert settings.MODE == 'TEST', f'Invalid mode: {settings.MODE}, miss TEST config.'
except AssertionError:
    exit(0)


@pytest_asyncio.fixture
async def client():
    from ..api.main import app
    async with LifespanManager(app) as manager:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=manager.app)) as client:
            yield client


class BaseTest:
    BASE_URL = "http://testserver"
    RECIPES_PREFIX = '/v1/recipes'
    ENDPOINT_STATUS_200 = "/status-ok"
    RECIPE_ID = '/1'


class TestGetRecipesAll(BaseTest):

    @pytest.mark.anyio
    async def test_status_code(self, client):
        """First simple test status route"""
        url = f"{self.BASE_URL}{self.RECIPES_PREFIX}{self.ENDPOINT_STATUS_200}"
        response = await client.get(url=url)
        assert response.status_code == codes.OK

    @pytest.mark.anyio
    async def test_get_all_recipes(self, client):
        """GET /v1/recipes all recipes"""
        url = f"{self.BASE_URL}{self.RECIPES_PREFIX}/"
        response = await client.get(url=url)
        assert response.status_code == codes.OK
