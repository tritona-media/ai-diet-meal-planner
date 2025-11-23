from src.services.llm_client import LLMClient
from src.models import PlanInput, RecommendInput
from src.models import RecipeResponse
from src.models import RecommendResponse
from .manager_agent import ManagerAgent

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.manager_agent = ManagerAgent()

    def plan(self, plan_input: PlanInput) -> RecipeResponse:
        prompt = (
            "You know all cooking recipes for all kinds of kitchens and diets.\n"
            f"I give you this base recipe idea: {plan_input.base_recipe}.\n"
            "Suggest one concrete recipe based on the recipe idea.\n"
            "For this concrete recipe return one JSON object that has the following structure:\n"
            "  title: name of the concrete recipe based on the recipe idea (it does not need to be the same name).\n"
            "  ingredients: a list of strings representing ingredients needed for the recipe.\n"
            "  steps: a list of JSON objects. One JSON object contains the ordered steps and instructions to cook the recipe.\n"
            "    step_number: an integer starting from 1. It represents the cooking step.\n"
            "    instruction: a short description of what to do in this step"
            "Respond ONLY with valid JSON."
        )
        recipe_response_dict = self.llm.call_model_json(prompt)
        return RecipeResponse(**recipe_response_dict)

    def recommend(self, recommend_input: RecommendInput) -> RecommendResponse:
        recipes = []
        ask_response = self.manager_agent.run(recommend_input)
        recipe_ideas = ask_response.suggestions[:recommend_input.recipe_count]
        for recipe_idea in recipe_ideas:
            recipe_response = self.plan(PlanInput(base_recipe=recipe_idea))
            recipes.append(recipe_response)
        return RecommendResponse(recipes=recipes)