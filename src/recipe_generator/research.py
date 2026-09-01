import logging
import time

from .mcp_client import search_multiple_recipes


logger = logging.getLogger(__name__)


def mcp_research(state):
    """
    Perform MCP research for all requested dishes.

    MCP searches are executed in parallel.

    Example:

        pizza  ─┐
        burger ─┤
        pasta  ─┤  → MCP
        kimchi ─┘

    The results remain in the same order as state.dishes.
    """

    total_start = time.perf_counter()

    logger.info(
        "MCP research started"
    )

    # ==================================================
    # GET DISHES
    # ==================================================

    queries = state.dishes

    if not queries:

        raise ValueError(
            "No dishes available for MCP research."
        )

    logger.info(
        "MCP research queries: %s",
        queries,
    )

    logger.info(
        "Number of MCP research queries: %d",
        len(queries),
    )

    # ==================================================
    # PARALLEL MCP SEARCH
    # ==================================================

    research_start = time.perf_counter()

    research_results = search_multiple_recipes(
        queries=queries,
        limit=1,
    )

    research_time = (
        time.perf_counter()
        - research_start
    )

    # ==================================================
    # VALIDATE RESULT COUNT
    # ==================================================

    if len(research_results) != len(queries):

        logger.warning(
            "Research result count (%d) does not match "
            "dish count (%d)",
            len(research_results),
            len(queries),
        )

    # ==================================================
    # LOG RESULTS
    # ==================================================

    for index, (
        dish,
        research,
    ) in enumerate(
        zip(
            queries,
            research_results,
        ),
        start=1,
    ):

        logger.info(
            "Research result %d/%d stored for dish: %s",
            index,
            len(queries),
            dish,
        )

        if research:

            logger.info(
                "Research result %d size: %d characters",
                index,
                len(research),
            )

        else:

            logger.warning(
                "No research result returned for dish: %s",
                dish,
            )

    # ==================================================
    # TOTAL TIME
    # ==================================================

    total_time = (
        time.perf_counter()
        - total_start
    )

    logger.info(
        "MCP research completed successfully"
    )

    logger.info(
        "Number of research results: %d",
        len(research_results),
    )

    logger.info(
        "MCP search time: %.2f seconds",
        research_time,
    )

    logger.info(
        "Total MCP research time: %.2f seconds",
        total_time,
    )

    # ==================================================
    # RETURN
    # ==================================================

    return {
        "research": research_results
    }