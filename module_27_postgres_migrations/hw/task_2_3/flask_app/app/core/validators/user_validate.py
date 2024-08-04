# Модель для валидации входящих и исходящих данных пользователя.

from typing import Optional

from pydantic import BaseModel, Field


class UserValidatorInput(BaseModel):
    name: str = Field(max_length=50)
    has_sale: Optional[bool] = None
    address: Optional[dict] = None
    coffee_id: Optional[int] = None

    class Config:
        extra = "ignore"
        from_attributes = True


class UserValidatorOutput(UserValidatorInput):
    id: int
