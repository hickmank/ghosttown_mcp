"""Simple MCP SDK client interaction."""

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main() -> None:
    """Utilize the local MCP server.

    Connect to the local MCP server, open a session, call the 'add_tool' method, and
    print the result.

    This function demonstrates a simple interaction with the MCP SDK client.
    """
    # 1) Connect to your local MCP server over HTTP
    async with streamablehttp_client(
        "http://localhost:4001/mcp/jsonrpc"
    ) as (read_stream, write_stream, _get_session_id):
        # 2) Open an MCP session
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # 3) Call your 'add_tool' method
            result = await session.call_tool(
                "add_tool",
                arguments={"a": 2, "b": 3}
            )

            # 4) Extract the structured or unstructured content
            if result.structuredContent is not None:
                # structuredContent is a Pydantic model or primitive type
                print("2 + 3 =", result.structuredContent)
            else:
                # result.content is a list of TextContent blocks
                text = result.content[0].text
                print("2 + 3 =", text)


if __name__ == "__main__":
    asyncio.run(main())

