from pydantic import BaseModel, Field, ConfigDict


class ValidateRecipeChartTable(BaseModel):
    recipe_id: int
    name: str = Field(min_length=2, max_length=50, description="Name of the dish")
    view: int = Field(gt=0, description='Popularity')
    time: int = Field(description="It takes time to make", title='minutes')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "recipe_id": 1,
                'name': "Pasta",
                'view': 777,
                'time': 15
            }
        }

    )


class ValidateRecipeInput(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="Name of the dish")
    time: int = Field(description="It takes time to make", title='minutes')
    ingredients: str = Field(min_length=3, max_length=250)
    description: str = Field(min_length=10, max_length=500, description='How can you make it?',
                             title='description process')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Spaghetti Aglio e Olio",
                "ingredients": "spaghetti, garlic, olive oil, red pepper, flakes, parsley",

                "time": 15,
                "description": "Cook spaghetti until al dente. In a pan, sauté garlic in olive oil. "
                               "Add red pepper flakes. Toss with cooked pasta and garnish with parsley."
            }
        }

    )


class ValidateRecipeOutput(ValidateRecipeInput):
    recipe_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "recipe_id": 1,
                "name": "Spaghetti Aglio e Olio",
                "ingredients": "spaghetti, garlic, olive oil, red pepper flakes, parsley",
                "time": 15,
                "description": "Cook spaghetti until al dente. In a pan, sauté garlic in olive oil. "
                               "Add red pepper flakes. Toss with cooked pasta and garnish with parsley."
            }
        }
    )


class ValidateCollectionRecipesOutput(BaseModel):
    recipes: list[ValidateRecipeOutput]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "recipes": [
                    {
                        "recipe_id": 1,
                        "description": "Simple preparation",
                        "ingredients": "water, tea, lemon",
                        "name": "tea with lemon",
                        "time": 10
                    },
                    {
                        "recipe_id": 2,
                        "description": "Quick and easy",
                        "ingredients": "water, tea",
                        "name": "red tea",
                        "time": 5
                    },
                    {
                        "recipe_id": 3,
                        "description": "Straightforward process",
                        "ingredients": "water, tea",
                        "name": "black tea",
                        "time": 10
                    },
                    {
                        "recipe_id": 4,
                        "description": "Effortless cooking",
                        "ingredients": "water, tea",
                        "name": "green tea",
                        "time": 5
                    },
                    {
                        "recipe_id": 5,
                        "description": "Minimal effort required",
                        "ingredients": "water, packed of tea",
                        "name": "packed-tea",
                        "time": 2
                    }
                ]
            }
        }

    )


class ValidateCollectionRecipesInput(BaseModel):
    recipes: list[ValidateRecipeInput]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "recipes": [
                    {
                        "description": "Simple preparation",
                        "ingredients": "water, tea, lemon",
                        "name": "tea with lemon",
                        "time": 10
                    },
                    {
                        "description": "Quick and easy",
                        "ingredients": "water, tea",
                        "name": "red tea",
                        "time": 5
                    },
                    {
                        "description": "Straightforward process",
                        "ingredients": "water, tea",
                        "name": "black tea",
                        "time": 10
                    },
                    {
                        "description": "Effortless cooking",
                        "ingredients": "water, tea",
                        "name": "green tea",
                        "time": 5
                    },
                    {
                        "description": "Minimal effort required",
                        "ingredients": "water, packed of tea",
                        "name": "packed-tea",
                        "time": 2
                    }
                ]
            }
        }

    )
