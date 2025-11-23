from pydantic import BaseModel

class InventoryInput(BaseModel):
    items: list[str]

class InventoryResponse(BaseModel):
    usable_items: list[str]
    message: str

class DietInput(BaseModel):
    items: list[str]
    diet: str

class DietResponse(BaseModel):
    compatible_items: list[str]
    suggested_recipe_ideas: list[str]

class AskInput(BaseModel):
    items: list[str]
    diet: str

class AskResponse(BaseModel):
    usable_items: list[str]
    diet_filtered: list[str]
    suggestions: list[str]

class PlanInput(BaseModel):
    base_recipe: str

class RecipeStep(BaseModel):
    step_number: int
    instruction: str

class RecipeResponse(BaseModel):
    title: str
    ingredients: list[str]
    steps: list[RecipeStep]

class RecommendInput(AskInput):
    recipe_count: int

class RecommendResponse(BaseModel):
    recipes: list[RecipeResponse]