from fastapi import APIRouter, Depends, status, HTTPException

from .validate_schemes.recipes_validate_model import ValidateRecipeOutput, ValidateRecipeInput, \
    ValidateRecipeChartTable, \
    ValidateCollectionRecipesOutput, ValidateCollectionRecipesInput
from .dependencies import get_all_recipes_from_db, get_recipe_by_id, create_recipe, create_many_recipes

router = APIRouter()


@router.get("/status-ok")
async def get_test_status():
    """Статус OK"""
    return {"status": "ok"}


@router.get("/", response_model=list[ValidateRecipeChartTable])
async def get_all_recipes(recipes: ValidateRecipeInput = Depends(get_all_recipes_from_db)):
    """Возвращает весь список рецептов."""
    return recipes


@router.get("/{recipe_id}", response_model=ValidateRecipeOutput)
async def get_recipe_by_id(recipe: ValidateRecipeInput = Depends(get_recipe_by_id)):
    """Возвращает рецепт по ID."""
    if recipe:
        return recipe

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found.')


@router.post("/", response_model=ValidateRecipeOutput,
             status_code=status.HTTP_201_CREATED)
async def create_new_recipes(recipe: ValidateRecipeInput = Depends(create_recipe)):
    """
    Создает рецепт и возвращает их.
    Лучше наверное отдавать только ID? Или это ситуативно? Просто кол-во данных будет кратно больше,
    в случае если гонять всю модель по сети.
    """
    return recipe


@router.post("/collection",
             response_model=ValidateCollectionRecipesOutput,
             status_code=status.HTTP_201_CREATED)
async def create_new_recipes(recipes: ValidateCollectionRecipesInput = Depends(create_many_recipes)):
    """Создает рецепты в нужном кол-ве. А затем возвращает их с ID."""
    return recipes
