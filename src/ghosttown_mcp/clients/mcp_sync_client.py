"""Synchronous MCP Client for FastMCP Tools."""

import asyncio
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPClientSync:
    """Synchronous wrapper for the MCP Python SDK (Streamable HTTP).

    Opens a short-lived MCP session, performs the initialize handshake,
    and invokes a tool by name—returning the structured result when available.
    """

    def __init__(self, url: str) -> None:
        """Initialize the client.

        Args:
            url (str): MCP endpoint URL, e.g. "http://localhost:4001/mcp/jsonrpc".
        """
        self.url = url

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> Any:
        """Synchronously invoke a tool.

        Args:
            tool (str): MCP tool name (for FastMCP, this is the function name,
                e.g. "add" if your tool is defined as `@mcp.tool() def add(...)`).
            arguments (dict[str, Any]): Keyword arguments to pass to the tool.

        Returns:
            Any: `structuredContent` if present, otherwise the first text block,
            otherwise `None`.

        Raises:
            RuntimeError: If the MCP call returns an error.
        """
        return asyncio.run(self._call_tool_async(tool, arguments))

    async def _call_tool_async(self, tool: str, arguments: dict[str, Any]) -> Any:
        async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                # 1) Handshake
                await session.initialize()

                # 2) (Optional) you could verify the tool exists:
                # tools = await session.list_tools()
                # if name not in [t.name for t in tools.tools]:
                #     raise RuntimeError(f"Tool '{name}' not found.
                #     Available: {[t.name for t in tools.tools]}")

                # 3) Call the tool
                result = await session.call_tool(tool, arguments=arguments)

                # 4) Prefer structuredContent; fall back to text content
                if result.structuredContent is not None:
                    return result.structuredContent

                if result.content:
                    return result.content[0].text

                return None
