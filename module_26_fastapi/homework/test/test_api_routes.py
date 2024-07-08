import pytest
from httpx import AsyncClient, codes, ASGITransport

# from pydantic import ValidationError
# from fastapi.exceptions import ResponseValidationError
# from ..api.main import app
from main import app
BASE_URL = "http://127.0.0.1:8000/"
RECIPES_URI_PREFIX = '/v1/recipes'
RECIPE_ID = '/1'

# dish_model = {'type_dish': "Pasta", 'view': 777, 'cooking_time': 15}

TRANSPORT = ASGITransport(app=app)

"""Создаем виртуальное окружение FastApi (TRANSPORT).
Это позволяет работать  с отдельным экземпляром приложения без нужны работы самого сервера."""


@pytest.mark.anyai
async def test_status_code():
    """First simple test  status route"""
    async with AsyncClient(transport=TRANSPORT, base_url=BASE_URL, follow_redirects=True) as test_route:
        response = await test_route.get('/status-ok')
        assert response.status_code == codes.OK

#
# class TestGetRecipesAll:
#
#
#
#     @pytest.mark.anyio
#     async def test_get_all_recipes(self, ):
#         """Test route /recipes  all dishes"""
#         async with AsyncClient(transport=TRANSPORT, base_url=BASE_URL, follow_redirects=True) as test_route:
#             response = await test_route.get(RECIPES_URI_PREFIX)
#
#             assert response.status_code == codes.OK
#             #
#             # try:
#             #     response_data = response.json()
#             # except ValidationError as e:
#             #     pytest.fail(f"Ошибка валидации данных: {e}")
#             # except ValueError:
#             #     pytest.fail("Ответ не является валидным JSON")
#             #
#
# # class TestGetOneRecipe:
# #
# #     @pytest.mark.anyio
# #     async def test_get_all_recipes_response_validation_error(self, ):
# #         """Test route /recipes/{recipe_id}  by dish id"""
# #         async with AsyncClient(transport=TRANSPORT, base_url=BASE_URL) as test_route:
# #             with pytest.raises(ResponseValidationError):
# #                 result = await test_route.get(RECIPE_ID)

