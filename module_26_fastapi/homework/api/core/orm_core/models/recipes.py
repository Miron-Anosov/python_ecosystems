from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

from .base import BaseORM


class RecipeORM(BaseORM):
    """
        recipe_id SERIAL NOT NULL,
        name VARCHAR(50) NOT NULL,
        time INTEGER NOT NULL,
        ingredients VARCHAR(250) NOT NULL,
        description VARCHAR(500) NOT NULL,
        PRIMARY KEY (recipe_id)
    """
    __tablename__ = 'recipe'
    recipe_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    time: Mapped[int]
    ingredients: Mapped[str] = mapped_column(String(length=250), nullable=False)

    description: Mapped[str] = mapped_column(String(length=500), nullable=False)
    chart_entries: Mapped[list["ChartRecipeORM"]] = relationship(back_populates="recipe")


class ChartRecipeORM(BaseORM):
    """
        chart_id SERIAL NOT NULL,
        recipe_id INTEGER NOT NULL,
        view INTEGER NOT NULL,
        PRIMARY KEY (chart_id),
        FOREIGN KEY(recipe_id) REFERENCES recipe (recipe_id)
    """
    __tablename__ = 'top_chart'

    chart_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.recipe_id"))
    view: Mapped[int] = mapped_column(default=1)

    recipe: Mapped["RecipeORM"] = relationship(back_populates='chart_entries')
