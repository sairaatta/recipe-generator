import asyncio
import logging
import time

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


logger = logging.getLogger(__name__)


# ============================================================
# MCP CONFIGURATION
# ============================================================

MCP_URL = "https://recipes.aidatanorge.no/mcp"


# ============================================================
# MCP CACHE
# ============================================================

_CACHE: dict[tuple[str, int], str] = {}


def _get_cached_result(
    query: str,
    limit: int,
) -> str | None:

    key = (
        query.strip().lower(),
        limit,
    )

    result = _CACHE.get(key)

    if result is not None:

        logger.info(
            "MCP cache HIT: %s",
            query,
        )

    return result


def _store_cached_result(
    query: str,
    limit: int,
    result: str,
) -> None:

    key = (
        query.strip().lower(),
        limit,
    )

    _CACHE[key] = result

    logger.info(
        "MCP result cached: %s",
        query,
    )


# ============================================================
# SINGLE MCP SEARCH
# ============================================================

async def _search_recipe_with_session(
    session: ClientSession,
    query: str,
    limit: int = 1,
) -> str:

    cached = _get_cached_result(
        query=query,
        limit=limit,
    )

    if cached is not None:
        return cached

    logger.info(
        "MCP searching recipe: %s",
        query,
    )

    start_time = time.perf_counter()

    try:

        result = await session.call_tool(
            "search_recipes",
            {
                "query": query,
                "limit": limit,
            },
        )

    except Exception as exc:

        logger.exception(
            "MCP search failed for '%s': %s",
            query,
            exc,
        )

        return ""

    elapsed = (
        time.perf_counter()
        - start_time
    )

    logger.info(
        "MCP search completed: %s in %.2f seconds",
        query,
        elapsed,
    )

    if not result.content:

        logger.warning(
            "MCP returned no content: %s",
            query,
        )

        return ""

    for content in result.content:

        if hasattr(content, "text"):

            text = content.text or ""

            if text:

                _store_cached_result(
                    query=query,
                    limit=limit,
                    result=text,
                )

            return text

    logger.warning(
        "MCP returned content without text: %s",
        query,
    )

    return ""


# ============================================================
# ASYNC PARALLEL MCP SEARCH
# ============================================================

async def _search_multiple_recipes_async(
    queries: list[str],
    limit: int = 1,
) -> list[str]:

    if not queries:
        return []

    total_start = time.perf_counter()

    logger.info(
        "Starting parallel MCP research for %d queries",
        len(queries),
    )

    # --------------------------------------------------------
    # NORMALIZE QUERIES
    # --------------------------------------------------------

    normalized_queries = [
        query.strip()
        for query in queries
        if query and query.strip()
    ]

    if not normalized_queries:
        return []

    logger.info(
        "MCP queries: %s",
        normalized_queries,
    )

    # --------------------------------------------------------
    # ONE MCP SESSION
    # --------------------------------------------------------

    session_start = time.perf_counter()

    try:

        async with streamable_http_client(
            MCP_URL
        ) as (
            read_stream,
            write_stream,
            _,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                session_time = (
                    time.perf_counter()
                    - session_start
                )

                logger.info(
                    "MCP session initialized in %.2f seconds",
                    session_time,
                )

                # ------------------------------------------------
                # CREATE TASKS
                # ------------------------------------------------

                tasks = []

                for index, query in enumerate(
                    normalized_queries,
                    start=1,
                ):

                    logger.info(
                        "Creating MCP task %d/%d: %s",
                        index,
                        len(normalized_queries),
                        query,
                    )

                    tasks.append(
                        _search_recipe_with_session(
                            session=session,
                            query=query,
                            limit=limit,
                        )
                    )

                # ------------------------------------------------
                # PARALLEL EXECUTION
                # ------------------------------------------------

                search_start = time.perf_counter()

                results = await asyncio.gather(
                    *tasks,
                    return_exceptions=True,
                )

                search_time = (
                    time.perf_counter()
                    - search_start
                )

                # ------------------------------------------------
                # PROCESS RESULTS
                # ------------------------------------------------

                research_results: list[str] = []

                for index, result in enumerate(
                    results,
                    start=1,
                ):

                    query = normalized_queries[
                        index - 1
                    ]

                    if isinstance(
                        result,
                        Exception,
                    ):

                        logger.error(
                            "MCP query failed: %s | error=%s",
                            query,
                            result,
                        )

                        research_results.append("")

                    else:

                        research_results.append(
                            result
                        )

                        logger.info(
                            "MCP query completed: %s",
                            query,
                        )

                logger.info(
                    "Parallel MCP searches completed in %.2f seconds",
                    search_time,
                )

    except Exception as exc:

        logger.exception(
            "MCP session failed: %s",
            exc,
        )

        return [
            ""
            for _ in normalized_queries
        ]

    # --------------------------------------------------------
    # TOTAL TIME
    # --------------------------------------------------------

    total_time = (
        time.perf_counter()
        - total_start
    )

    logger.info(
        "Parallel MCP research completed: %d results in %.2f seconds",
        len(research_results),
        total_time,
    )

    return research_results


# ============================================================
# SYNC SINGLE SEARCH
# ============================================================

def search_recipes(
    query: str,
    limit: int = 1,
) -> str:

    if not query or not query.strip():

        logger.warning(
            "search_recipes called with empty query"
        )

        return ""

    logger.info(
        "Single MCP recipe search: %s",
        query,
    )

    results = asyncio.run(
        _search_multiple_recipes_async(
            queries=[query],
            limit=limit,
        )
    )

    return (
        results[0]
        if results
        else ""
    )


# ============================================================
# SYNC PARALLEL BATCH SEARCH
# ============================================================

def search_multiple_recipes(
    queries: list[str],
    limit: int = 1,
) -> list[str]:

    logger.info(
        "Starting parallel MCP batch research for %d queries",
        len(queries),
    )

    if not queries:
        return []

    normalized_queries = [
        query.strip()
        for query in queries
        if query and query.strip()
    ]

    if not normalized_queries:
        return []

    logger.info(
        "MCP batch queries: %s",
        normalized_queries,
    )

    results = asyncio.run(
        _search_multiple_recipes_async(
            queries=normalized_queries,
            limit=limit,
        )
    )

    logger.info(
        "Parallel MCP batch research completed: %d results",
        len(results),
    )

    return results