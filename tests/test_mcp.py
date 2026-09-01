import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_URL = "https://recipes.aidatanorge.no/mcp"


async def main():

    print("=" * 60)
    print("PHASE 9 - FOOD RECIPE MCP TEST")
    print("=" * 60)

    print("\nConnecting to:")
    print(MCP_URL)

    try:

        # ==================================================
        # 1. CONNECT TO MCP
        # ==================================================

        async with streamable_http_client(MCP_URL) as (
            read_stream,
            write_stream,
        ):

            print("\n✓ HTTP connection established")

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                # ==================================================
                # 2. INITIALIZE MCP SESSION
                # ==================================================

                print("\nInitializing MCP session...")

                await session.initialize()

                print("✓ MCP session initialized")

                # ==================================================
                # 3. LIST AVAILABLE TOOLS
                # ==================================================

                print("\n" + "-" * 60)
                print("AVAILABLE MCP TOOLS")
                print("-" * 60)

                tools_result = await session.list_tools()

                tool_names = []

                for tool in tools_result.tools:

                    tool_names.append(tool.name)

                    print(f"\nTool: {tool.name}")

                    if tool.description:
                        print(
                            f"Description: "
                            f"{tool.description}"
                        )

                assert "search_recipes" in tool_names

                print(
                    "\n✓ search_recipes tool is available"
                )

                # ==================================================
                # 4. SEQUENTIAL MULTI-QUERY TEST
                # ==================================================

                print("\n" + "-" * 60)
                print("SEQUENTIAL RECIPE SEARCH TEST")
                print("-" * 60)

                queries = [
                    "pizza",
                    "burger",
                    "pasta",
                ]

                results = []

                # IMPORTANT:
                # All three searches use the SAME MCP session.

                for index, query in enumerate(
                    queries,
                    start=1,
                ):

                    print(
                        f"\nSearch {index}/{len(queries)}: "
                        f"{query}"
                    )

                    result = await session.call_tool(
                        "search_recipes",
                        {
                            "query": query,
                            "limit": 3,
                        },
                    )

                    assert result.content

                    query_result = ""

                    for content in result.content:

                        if hasattr(content, "text"):
                            query_result += content.text

                        else:
                            query_result += str(content)

                    results.append(query_result)

                    print(
                        f"✓ Search {index} completed"
                    )

                    print(
                        f"Result size: "
                        f"{len(query_result)} characters"
                    )

                # ==================================================
                # 5. VALIDATE RESULTS
                # ==================================================

                print("\n" + "-" * 60)
                print("VALIDATION")
                print("-" * 60)

                assert len(results) == len(queries)

                for index, result in enumerate(
                    results,
                    start=1,
                ):

                    assert result

                    print(
                        f"✓ Query {index} returned "
                        f"research data"
                    )

                print(
                    "\n✓ All sequential MCP searches "
                    "completed using ONE session"
                )

        # ==================================================
        # 6. SESSION CLOSED
        # ==================================================

        print("\n✓ MCP session closed")

        print("\n" + "=" * 60)
        print("✓ PHASE 9 MCP TEST PASSED")
        print("=" * 60)

    except Exception as e:

        print("\n" + "=" * 60)
        print("✗ PHASE 9 MCP TEST FAILED")
        print("=" * 60)

        print(f"\nError type: {type(e).__name__}")
        print(f"Error: {e}")

        raise


if __name__ == "__main__":
    asyncio.run(main())