from typing import Iterable

from sqlalchemy import text, Sequence
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from .models.recipes import RecipeORM, ChartRecipeORM
from ..validate_schemes.recipes_validate_model import ValidateRecipeInput, ValidateCollectionRecipesInput


class RecipeCRUD:

    @staticmethod
    async def select_all_recipes_from_db(async_session: AsyncSession) -> Result:
        """
        Возвращает все элементы из таблицы с рецептами:
           - название
           - количество просмотров
           - время готовки (в минутах)
        """
        top_table = text(
            """
            SELECT  
                recipe.name AS name, recipe.time AS time, 
                top_chart.recipe_id AS recipe_id, top_chart.view AS view
            FROM  recipe
            JOIN top_chart
                ON top_chart.recipe_id = recipe.recipe_id
            ORDER BY view DESC, time ASC
            """
        )
        return await async_session.execute(top_table)

    @staticmethod
    async def select_by_id(async_session: AsyncSession, recipe_id: int) -> RecipeORM | None:
        """
        Возвращает рецепт из таблицы recipe по ID. Или None в случе отсутствия.
            - название
            - время готовки
            - список ингредиентов
            - текстовое описание
        """
        recipe = await async_session.get(RecipeORM, recipe_id)
        await async_session.close()
        return recipe

    @staticmethod
    async def insert_recipe(async_session: AsyncSession, recipe: ValidateRecipeInput) -> RecipeORM:
        """
        Добавляем новый рецепт в таблицу recipe.
        """
        recipe_orm = RecipeORM(**recipe.model_dump())
        async_session.add(recipe_orm)
        await async_session.commit()
        return recipe_orm

    @staticmethod
    async def update_chart(async_session: AsyncSession, recipe_id: int) -> None:
        """Обновляем статистику просмотров рецепта view += 1 в top_chart"""

        async with async_session.begin():
            chart = await async_session.get(ChartRecipeORM, recipe_id)
            chart.view += 1
            async_session.add(chart)

    @staticmethod
    async def insert_chart(async_session: AsyncSession,
                           recipes: list[RecipeORM] | RecipeORM) -> None:
        """
        Добавляем рецепты в таблицу top_chart для отслеживания статистики просмотров.
        """

        if isinstance(recipes, Iterable):
            for recipe in recipes:
                new_chart = ChartRecipeORM(recipe_id=recipe.recipe_id)
                async_session.add(new_chart)
        else:
            new_chart = ChartRecipeORM(recipe_id=recipes.recipe_id)
            async_session.add(new_chart)
        await async_session.commit()

    @staticmethod
    async def inset_many_recipes(
            async_session: AsyncSession,
            recipes: ValidateCollectionRecipesInput
    ) -> Sequence[RecipeORM]:

        """
        Создаем в таблице top_chart N рецептов.
        """

        new_recipes: list = recipes.model_dump().get('recipes')
        stmt = insert(RecipeORM).values(new_recipes).returning(RecipeORM)
        result: Result[tuple[RecipeORM]] = await async_session.execute(stmt)
        await async_session.commit()
        return result.scalars().all()


crud = RecipeCRUD()
