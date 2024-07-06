from fastapi import Depends
from .orm_core import engine, crud
from .validate_schemes.recipes_validate_model import ValidateRecipeInput, ValidateCollectionRecipesInput


def get_session():
    """Как лучше обращаться к сессии?"""
    return engine.create_async_session_maker


async def get_recipe_by_id(recipe_id: int, session=Depends(get_session)):
    """Возвращает рецепт по ID"""
    recipe = await crud.select_by_id(async_session=session, recipe_id=recipe_id)
    if recipe:
        await crud.update_chart(async_session=session, recipe_id=recipe_id)
    return recipe


async def get_all_recipes_from_db(session=Depends(get_session)):
    """Возвращает все рецепты"""
    return await crud.select_all_recipes_from_db(session)


async def create_recipe(recipe: ValidateRecipeInput, async_session=Depends(get_session)):
    new_recipe = await crud.insert_recipe(async_session=async_session, recipe=recipe)
    await crud.insert_chart(async_session=async_session, recipes=new_recipe)
    return new_recipe


async def create_many_recipes(recipes: ValidateCollectionRecipesInput, async_session=Depends(get_session)):
    new_recipes = await crud.inset_many_recipes(async_session=async_session, recipes=recipes)
    await crud.insert_chart(async_session=async_session, recipes=new_recipes)
    recipes: dict = {'recipes': new_recipes}
    return recipes
