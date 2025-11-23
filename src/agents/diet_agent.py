from src.services.llm_client import LLMClient
from src.models import DietInput
from src.models import DietResponse
from src.app_logging import get_logger

class DietAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.logger = get_logger("diet_agent")

    def run(self, diet_input: DietInput) -> DietResponse:
        self.logger.info(f"diet input: {diet_input}")
        prompt = (
            f"You are a nutrition and cooking expert. Given a list of ingredients:\n"
            f"{diet_input.items}\n"
            f"Remove empty, blank or invalid entries from the list of ingredients.\n"
            f"Keep all ingredients that fit the following diet: {diet_input.diet}.\n"
            "Return a JSON object with:\n"
            f"  compatible_items: an array of strings representing the ingredients fitting the provided diet.\n"
            f"  suggested_recipe_ideas: a list of strings representing recipe ideas for the {diet_input.diet} diet compatible ingredients. Just give me the title of the recipe ideas, no description or details.\n"
            "Respond ONLY with valid JSON."
        )
        diet_response_dict = self.llm.call_model_json(prompt)
        self.logger.info(f"diet output: {diet_response_dict}")
        return DietResponse(**diet_response_dict)
