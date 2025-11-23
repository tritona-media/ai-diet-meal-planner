from src.services.llm_client import LLMClient
from src.models import InventoryInput
from src.models import InventoryResponse
from src.app_logging import get_logger

class InventoryAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.logger = get_logger("inventory_agent")

    def run(self, inventory_input: InventoryInput) -> InventoryResponse:
        self.logger.info(f"inventory input: {inventory_input}")
        prompt = (
            f"You are a kitchen assistant. Given the JSON array of ingredients:\n"
            f"{inventory_input.model_dump_json()}\n"
            "Return a JSON object with:\n"
            "  usable_items: an array of ingredients that are non-empty and suitable for cooking (remove blank or invalid entries),\n"
            "  message: a short confirmation string.\n"
            "Respond ONLY with valid JSON."
        )
        inventory_response_dict = self.llm.call_model_json(prompt)
        self.logger.info(f"inventory output: {inventory_response_dict}")
        return InventoryResponse(**inventory_response_dict)
