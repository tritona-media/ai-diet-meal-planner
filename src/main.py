from fastapi import FastAPI, Depends

from src.models import InventoryInput, InventoryResponse, DietResponse, DietInput, AskInput, AskResponse, PlanInput, RecipeResponse, RecommendInput, RecommendResponse
from src.agents.manager_agent import ManagerAgent
from src.agents.inventory_agent import InventoryAgent
from src.agents.diet_agent import DietAgent
from src.agents.planner_agent import PlannerAgent

from src.app_logging import get_logger

app = FastAPI()

logger = get_logger("app")

manager_agent = ManagerAgent()
diet_agent = DietAgent()
inventory_agent = InventoryAgent()
planner_agent = PlannerAgent()

def get_manager_agent():
    return manager_agent

def get_diet_agent():
    return diet_agent

def get_inventory_agent():
    return inventory_agent

def get_planner_agent():
    return planner_agent

@app.get("/")
async def root():
    return {"message": "Success!"}

@app.post("/inventory", response_model=InventoryResponse)
async def filter_usable_items(
        inventory_input: InventoryInput,
        agent: InventoryAgent = Depends(get_inventory_agent)
    ):
    return agent.run(inventory_input)


@app.post("/diet", response_model=DietResponse)
async def suggest_recipes(
        diet_input: DietInput,
        agent: DietAgent = Depends(get_diet_agent)
    ):
    return agent.run(diet_input)

@app.post("/ask", response_model=AskResponse)
async def ask_for_recipes(
        ask_input: AskInput,
        agent: ManagerAgent = Depends(get_manager_agent)
    ):
    logger.info(f"Received /ask request: items={ask_input.items}, diet={ask_input.diet}")
    result = agent.run(ask_input)
    logger.info(f"/ask response: suggestions={result.suggestions}")
    return result

@app.post("/plan", response_model=RecipeResponse)
async def plan_recipes(
        plan_input: PlanInput,
        agent: PlannerAgent = Depends(get_planner_agent)
):
    logger.info(f"Received /plan request: base_recipe={plan_input.base_recipe}")
    result = agent.plan(plan_input)
    logger.info(f"/plan response: title={result.title}")
    return result

@app.post("/recommend", response_model=RecommendResponse)
async def recommend_recipes(
        recommend_input: RecommendInput,
        agent: PlannerAgent = Depends(get_planner_agent)
):
    logger.info(f"Received /recommend request: items={recommend_input.items}, "
                f"diet={recommend_input.diet}, recipe_count={recommend_input.recipe_count}")
    result = agent.recommend(recommend_input)
    logger.info(f"/recommend response: recipe_count={len(result.recipes)}")
    return result