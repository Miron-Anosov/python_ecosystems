import pytest
from httpx import codes
import httpx
import pytest_asyncio

from enum import Enum
from asgi_lifespan import LifespanManager

from ..api.core.orm_core import BaseORM
from ..api.core.orm_core import AsyncCoreDB
from ..api.core.settings import settings
from ..api.core.validate_schemes.recipes_validate_model import ValidateRecipeOutput

try:
    assert settings.MODE == 'TEST', f'Invalid mode: {settings.MODE}, miss TEST config.'
except AssertionError:
    exit(0)


db = AsyncCoreDB(url=settings.host_database_sqlalchemy, echo=settings.ECHO)


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
    async with LifespanManager(app):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
            yield client


class RecipeConstants(Enum):
    LEN_EMPTY = 0
    NEW_RECIPE_CREATED = 1
    NEW_RECIPES_CREATED = 5
    COUNT_VIEW_ONE = 1
    COUNT_VIEW_TWO = 2


class RecipesCollection(Enum):
    MODEL_RECIPE_VALID = {
        "description": "Cook spaghetti until al dente. In a pan, sauté garlic in olive oil. "
                       "Add red pepper flakes. Toss with cooked pasta and garnish with parsley.",
        "ingredients": "spaghetti, garlic, olive oil, red pepper, flakes, parsley",
        "name": "Spaghetti Aglio e Olio",
        "time": 15
    }
    MODEL_RECIPE_INVALID = {
        "description": "Cook spaghetti until al dente. In a pan, sauté garlic in olive oil. "
                       "Add red pepper flakes. Toss with cooked pasta and garnish with parsley.",
        "ingredients": "spaghetti, garlic, olive oil, red pepper, flakes, parsley",
        "name": "Spaghetti Aglio e Olio",
        "time": 'fifteen'
    }


class URLs(Enum):
    BASE_URL = "http://testserver/v1/recipes/"
    ENDPOINT_STATUS_200 = f"{BASE_URL}status-ok"
    GET_RECIPE_BY_ID = f"{BASE_URL}1"


class TestGetRecipesAll:

    @pytest.mark.anyio
    async def test_status_code(self, client):
        """First simple test status route"""
        response = await client.get(url=URLs.ENDPOINT_STATUS_200.value)
        assert response.status_code == codes.OK

    @pytest.mark.anyio
    async def test_get_all_recipes(self, client):
        """GET /v1/recipes all recipes"""
        response = await client.get(url=URLs.BASE_URL.value)
        assert response.status_code == codes.OK

    @pytest.mark.anyio
    async def test_get_all_recipes_again(self, client):
        """GET /v1/recipes all recipes"""
        response = await client.get(url=URLs.BASE_URL.value)
        assert response.status_code == codes.OK
        assert len(response.json()) == RecipeConstants.LEN_EMPTY.value

    @pytest.mark.anyio
    async def test_post_recipe_successful_valid_model(self, client):
        response = await client.post(url=URLs.BASE_URL.value, json=RecipesCollection.MODEL_RECIPE_VALID.value)

        assert response.status_code == codes.CREATED
        assert ValidateRecipeOutput(**response.json()), 'Invalid model'

    @pytest.mark.anyio
    async def test_post_recipe_fail_exc_422(self, client):
        response = await client.post(url=URLs.BASE_URL.value, json=RecipesCollection.MODEL_RECIPE_INVALID.value)
        assert response.status_code == codes.UNPROCESSABLE_ENTITY

    @pytest.mark.anyio
    async def test_post_recipe_successful_one_model_in_db(self, client):
        await client.post(url=URLs.BASE_URL.value, json=RecipesCollection.MODEL_RECIPE_VALID.value)
        response = await client.get(url=URLs.BASE_URL.value)

        assert len(response.json()) == RecipeConstants.NEW_RECIPE_CREATED.value

    @pytest.mark.anyio
    async def test_get_recipes_bt_id_fail_exc_404(self, client):
        response = await client.get(url=URLs.GET_RECIPE_BY_ID.value)
        assert response.status_code == codes.NOT_FOUND

    @pytest.mark.anyio
    async def test_get_recipes_bt_id_successful_count_view(self, client):
        count_view_key = 'view'

        await client.post(url=URLs.BASE_URL.value, json=RecipesCollection.MODEL_RECIPE_VALID.value)
        response = await client.get(url=URLs.BASE_URL.value)
        response_data: list[dict] = response.json()
        count_call_by_id: int = response_data.pop().get(count_view_key)

        await client.get(url=URLs.GET_RECIPE_BY_ID.value)
        response_two = await client.get(url=URLs.BASE_URL.value)
        response_data_two: list[dict] = response_two.json()
        count_call_by_id_two: int = response_data_two.pop().get(count_view_key)

        assert count_call_by_id == RecipeConstants.COUNT_VIEW_ONE.value
        assert count_call_by_id_two == RecipeConstants.COUNT_VIEW_TWO.value

