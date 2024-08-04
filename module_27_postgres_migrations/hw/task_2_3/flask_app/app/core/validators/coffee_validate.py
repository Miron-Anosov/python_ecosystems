# Модель для валидации входящих и исходящих данных кофе.
from pydantic import BaseModel, Field, AliasChoices


class CoffeeValidatorInput(BaseModel):
    title: str = Field(max_length=200, validation_alias=AliasChoices("blend_name", "title"))
    origin: str | None = Field(max_length=200, default=None)
    intensifier: str = Field(max_length=100)
    notes: list[str] | None = None

    class Config:
        extra = "ignore"
        from_attributes = True


class CoffeeValidatorOutput(CoffeeValidatorInput):
    id: int
