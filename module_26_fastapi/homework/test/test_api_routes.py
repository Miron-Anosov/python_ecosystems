import pytest
from httpx import codes
import httpx
import pytest_asyncio


from asgi_lifespan import LifespanManager

from ..api.core.orm_core.models.base import BaseORM
from ..api.core.settings import setting
from ..api.core.orm_core.engine import AsyncCoreDB

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


DATABASE_URL = setting.test.host_database_sqlalchemy
db = AsyncCoreDB(url=DATABASE_URL, echo=True)

try:
    assert setting.test.MODE == 'TEST', 'Research our env'
except AssertionError:
    exit(0)


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = db.async_engine
    yield engine
    await db.async_engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_session(engine):
    async_scoped_session_maker = db.async_scoped_session()
    session = async_scoped_session_maker()
    try:
        yield session
    finally:
        await session.close()
        await async_scoped_session_maker.remove()


@pytest_asyncio.fixture
async def app():
    from ..api.main import app
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(app):
    async with LifespanManager(app) as manager:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
            yield client


@pytest.mark.usefixtures("client")
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
        print(response)
        print(response.url)
        assert response.status_code == codes.OK
