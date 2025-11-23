from src.agents.inventory_agent import InventoryAgent
from src.agents.diet_agent import DietAgent
from src.models import AskInput, InventoryInput, DietInput
from src.models import AskResponse


class ManagerAgent:
    def __init__(self):
        self.inventory_agent = InventoryAgent()
        self.diet_agent = DietAgent()

    def run(self, ask_input: AskInput) -> AskResponse:
        inventory_input = InventoryInput(items=ask_input.items)
        inventory_response_dict = self.inventory_agent.run(inventory_input)
        diet_input = DietInput(items=inventory_response_dict.usable_items, diet=ask_input.diet)
        diet_response_dict = self.diet_agent.run(diet_input)
        return AskResponse(
            usable_items=inventory_response_dict.usable_items,
            diet_filtered=diet_response_dict.compatible_items,
            suggestions=diet_response_dict.suggested_recipe_ideas
        )
