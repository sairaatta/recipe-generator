import logging

from langgraph.graph import StateGraph, START, END

from .state import RecipeState
from .input_decision import input_decision
from .orchestrator import orchestrator
from .research import mcp_research
from .chefs import chef_node
from .cost_estimator import estimate_costs


logger = logging.getLogger(__name__)


# ============================================================
# CHEF ROUTING
# ============================================================

def route_after_chef(state: RecipeState):
    """
    Decide whether another dish needs to be processed.

    Example:

        dishes = ["pizza", "burger", "pasta"]

        After pizza:
            current_dish_index = 1
            -> chef

        After burger:
            current_dish_index = 2
            -> chef

        After pasta:
            current_dish_index = 3
            -> collect
    """

    current_index = state.current_dish_index
    total_dishes = len(state.dishes)

    logger.info(
        "Chef routing | current_index=%d | total_dishes=%d",
        current_index,
        total_dishes,
    )

    if current_index < total_dishes:

        logger.info(
            "More dishes remaining. Routing back to chef_node."
        )

        return "chef"

    logger.info(
        "All dishes processed. Routing to collect."
    )

    return "collect"


# ============================================================
# COLLECT RECIPES
# ============================================================

def collect_recipes(state: RecipeState):
    """
    Final collection step after all dishes have been processed.

    Recipes are already stored in state.recipes by chef_node.
    """

    logger.info(
        "Collecting recipes"
    )

    recipe_count = len(state.recipes)

    logger.info(
        "Collected %d recipes",
        recipe_count,
    )

    return {
        "status": "recipes_generated",
        "next_step": "cost_estimator",
    }


# ============================================================
# BUILD GRAPH
# ============================================================

def build_recipe_graph():
    """
    Build and compile the recipe generation graph.

    Flow:

        START
          ↓
      input_decision
          ↓
      orchestrator
          ↓
      mcp_research
          ↓
       chef_node
          ↓
      route_after_chef
        ↙       ↘
      chef     collect
       ↑          ↓
       │      estimate_costs
       │          ↓
       └──────── END
    """

    logger.info(
        "Building LangGraph"
    )

    builder = StateGraph(
        RecipeState
    )

    # ========================================================
    # ADD NODES
    # ========================================================

    builder.add_node(
        "input_decision",
        input_decision,
    )

    builder.add_node(
        "orchestrator",
        orchestrator,
    )

    builder.add_node(
        "mcp_research",
        mcp_research,
    )

    builder.add_node(
        "chef",
        chef_node,
    )

    builder.add_node(
        "collect",
        collect_recipes,
    )

    builder.add_node(
        "estimate_costs",
        estimate_costs,
    )

    # ========================================================
    # START → INPUT DECISION
    # ========================================================

    builder.add_edge(
        START,
        "input_decision",
    )

    # ========================================================
    # INPUT DECISION → ORCHESTRATOR
    # ========================================================

    builder.add_edge(
        "input_decision",
        "orchestrator",
    )

    # ========================================================
    # ORCHESTRATOR → MCP RESEARCH
    # ========================================================

    builder.add_edge(
        "orchestrator",
        "mcp_research",
    )

    # ========================================================
    # MCP RESEARCH → FIRST CHEF
    # ========================================================

    builder.add_edge(
        "mcp_research",
        "chef",
    )

    # ========================================================
    # CHEF → ROUTING
    # ========================================================

    builder.add_conditional_edges(
        "chef",
        route_after_chef,
        {
            "chef": "chef",
            "collect": "collect",
        },
    )

    # ========================================================
    # COLLECT → COST ESTIMATION
    # ========================================================

    builder.add_edge(
        "collect",
        "estimate_costs",
    )

    # ========================================================
    # COST ESTIMATION → END
    # ========================================================

    builder.add_edge(
        "estimate_costs",
        END,
    )

    # ========================================================
    # COMPILE
    # ========================================================

    graph = builder.compile()

    logger.info(
        "LangGraph compiled successfully"
    )

    return graph

