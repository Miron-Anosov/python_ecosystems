import pytest
from httpx import AsyncClient, codes, ASGITransport
from pydantic import ValidationError

from ..api.main import app
from ..api.routes.validate_schemes.recipes_validate_model import ListValidateRecipeHTTP


BASE_URL = "http://127.0.0.1:8000/demo"
GET_ALL_RECIPES_URI_PREFIX = '/recipes'

dish_model = {'type_dish': "Pasta", 'view': 777, 'cooking_time': 15}
transport = ASGITransport(app=app)


@pytest.mark.anyio
async def test_get_all_recipes():
    """Successful test route: /recipes  code == 200"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as test_route:
        response = await test_route.get('/')
        assert response.status_code == codes.OK


@pytest.mark.anyio
async def test_get_all_recipes_responses_model():
    async with AsyncClient(transport=transport, base_url=BASE_URL) as test_route:
        response = await test_route.get(GET_ALL_RECIPES_URI_PREFIX)
        with pytest.raises(ValidationError):
            ListValidateRecipeHTTP.model_validate_json(response.json())
