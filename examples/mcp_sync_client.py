"""Synchronous MCP-SDK client wrapper example."""

import asyncio

# Core MCP SDK pieces
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPClientSync:
    """Synchronous wrapper around the MCP Python SDK.

    Connects over HTTP+SSE, performs initialize/tool-discovery,
    and lets you call tools in plain sync code.
    """

    def __init__(self, url: str) -> None:
        """Initialize the MCP client with the server URL.

        Args:
            url (str): The MCP server's JSON-RPC/SSE endpoint,
                       e.g. "http://localhost:4000/jsonrpc"
        """
        self.url = url

    def call_tool(self, tool_name: str, **arguments) -> str:
        """Synchronously invoke a tool by name with keyword arguments.

        Under the hood it starts an asyncio loop, opens an SSE session,
        runs the initialize handshake, and calls the tool.

        Args:
            tool_name (str): The name of the MCP tool to call (e.g. "add_tool")
            **arguments: Keyword arguments to pass to the tool

        Returns:
            The tool's result (structuredContent if present,
            else falls back to the first text block)
        """
        return asyncio.run(self._call_tool_async(tool_name, arguments))

    async def _call_tool_async(
            self,
            tool_name: str,
            arguments: dict
            ) -> str:
        """Asynchronous helper to call a tool by name with arguments."""
        # 1) Open a streaming HTTP(SSE) connection to the MCP server.
        async with streamablehttp_client(
            self.url
        ) as (read_stream, write_stream, _get_session_id):
            # 2) Create an MCP session on those streams
            async with ClientSession(read_stream, write_stream) as session:
                # 3) Perform the mandatory initialize handshake
                await session.initialize()

                # 4) Invoke the tool by name
                result = await session.call_tool(
                    tool_name,
                    arguments=arguments
                )

                # 5) Return structuredContent if the server provided it,
                #    otherwise return the first text block
                if result.structuredContent is not None:
                    return result.structuredContent
                if result.content:
                    # content is a list of TextContent objects
                    return result.content[0].text
                return None


# Example usage when run as a script:
if __name__ == "__main__":
    client = MCPClientSync("http://localhost:4000/jsonrpc")

    # This will call your add_tool(a=5, b=7) and print 12
    print("5 + 7 =", client.call_tool("add_tool", a=5, b=7)['value'])
