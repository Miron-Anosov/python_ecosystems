from typing import Iterable

from sqlalchemy import text, Sequence
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.engine import Result
from .models.recipes import RecipeORM, ChartRecipeORM
from ..validate_schemes.recipes_validate_model import ValidateRecipeInput, ValidateCollectionRecipesInput


class RecipeCRUD:

    @staticmethod
    async def select_all_recipes_from_db(async_session: async_sessionmaker[AsyncSession]) -> Result:
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

        async with async_session() as session:
            return await session.execute(top_table)

    @staticmethod
    async def select_by_id(async_session: async_sessionmaker[AsyncSession], recipe_id: int) -> RecipeORM | None:
        """
        Возвращает рецепт из таблицы recipe по ID. Или None в случе отсутствия.
            - название
            - время готовки
            - список ингредиентов
            - текстовое описание
        """
        async with async_session() as con:
            return await con.get(RecipeORM, recipe_id)

    @staticmethod
    async def insert_recipe(async_session: async_sessionmaker[AsyncSession], recipe: ValidateRecipeInput) -> RecipeORM:
        """
        Добавляем новый рецепт в таблицу recipe.
        """
        async with async_session() as session:
            recipe_orm = RecipeORM(**recipe.model_dump())
            session.add(recipe_orm)
            await session.commit()
            return recipe_orm

    @staticmethod
    async def update_chart(async_session: async_sessionmaker[AsyncSession], recipe_id: int) -> None:
        """Обновляем статистику просмотров рецепта view += 1 в top_chart"""
        async with async_session() as session:
            async with session.begin():
                chart = await session.get(ChartRecipeORM, recipe_id)
                chart.view += 1
                session.add(chart)

    @staticmethod
    async def insert_chart(async_session: async_sessionmaker[AsyncSession],
                           recipes: list[RecipeORM] | RecipeORM) -> None:
        """
        Добавляем рецепты в таблицу top_chart для отслеживания статистики просмотров.
        """

        async with async_session() as session:
            if isinstance(recipes, Iterable):
                for recipe in recipes:
                    new_chart = ChartRecipeORM(recipe_id=recipe.recipe_id)
                    session.add(new_chart)
            else:
                new_chart = ChartRecipeORM(recipe_id=recipes.recipe_id)
                session.add(new_chart)
            await session.commit()

    @staticmethod
    async def inset_many_recipes(
            async_session: async_sessionmaker[AsyncSession],
            recipes: ValidateCollectionRecipesInput
    ) -> Sequence[RecipeORM]:

        """
        Создаем в таблице top_chart N рецептов.
        """

        new_recipes: list = recipes.model_dump().get('recipes')
        async with async_session() as session:
            stmt = insert(RecipeORM).values(new_recipes).returning(RecipeORM)
            result: Result[tuple[RecipeORM]] = await session.execute(stmt)
            await session.commit()
            return result.scalars().all()


crud = RecipeCRUD()
