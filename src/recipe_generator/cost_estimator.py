import logging

from .state import RecipeState


logger = logging.getLogger(__name__)


# ------------------------------------------------------------
# Token pricing
# ------------------------------------------------------------

# Example pricing.
# Change these according to the pricing model
# you want to report for your project.

INPUT_PRICE_PER_1K = 0.001
OUTPUT_PRICE_PER_1K = 0.002


def calculate_token_cost(
    input_tokens: int,
    output_tokens: int,
) -> float:

    input_cost = (
        input_tokens / 1000
    ) * INPUT_PRICE_PER_1K

    output_cost = (
        output_tokens / 1000
    ) * OUTPUT_PRICE_PER_1K

    return input_cost + output_cost


# ------------------------------------------------------------
# Cost Estimator
# ------------------------------------------------------------

def estimate_costs(state: RecipeState):

    logger.info(
        "Phase 13: Token cost estimation started"
    )

    costs = {}

    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    total_cost = 0.0

    # --------------------------------------------------------
    # Process dynamic chef usage
    # --------------------------------------------------------

    for index, usage in enumerate(
        state.chef_usage,
        start=1,
    ):

        if usage is None:
            continue

        # ----------------------------------------------------
        # Support your current usage format
        #
        # {
        #     "input": 300,
        #     "output": 552,
        #     "total": 852
        # }
        #
        # and also the newer format:
        #
        # {
        #     "input_tokens": 300,
        #     "output_tokens": 552,
        #     "total_tokens": 852
        # }
        # ----------------------------------------------------

        input_tokens = usage.get(
            "input_tokens",
            usage.get("input", 0),
        )

        output_tokens = usage.get(
            "output_tokens",
            usage.get("output", 0),
        )

        total_tokens_for_call = usage.get(
            "total_tokens",
            usage.get(
                "total",
                input_tokens + output_tokens,
            ),
        )

        # ----------------------------------------------------
        # Calculate cost
        # ----------------------------------------------------

        cost = calculate_token_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        chef_name = f"Chef {index}"

        costs[chef_name] = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens_for_call,
            "estimated_cost": cost,
        }

        # ----------------------------------------------------
        # Update totals
        # ----------------------------------------------------

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_tokens += total_tokens_for_call
        total_cost += cost

        logger.info(
            "%s | input=%d | output=%d | total=%d | cost=%.6f",
            chef_name,
            input_tokens,
            output_tokens,
            total_tokens_for_call,
            cost,
        )

    # --------------------------------------------------------
    # Add overall totals
    # --------------------------------------------------------

    costs["total"] = {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": total_cost,
    }

    logger.info(
        "Total input tokens: %d",
        total_input_tokens,
    )

    logger.info(
        "Total output tokens: %d",
        total_output_tokens,
    )

    logger.info(
        "Total tokens: %d",
        total_tokens,
    )

    logger.info(
        "Total estimated cost: %.6f",
        total_cost,
    )

    logger.info(
        "Phase 13: Token cost estimation completed"
    )

    return {
        "cost_estimates": costs,
    }