"""ReAct agent built on LangGraph+Ollama that interacts with FastMCP server."""

import asyncio

from langchain_ollama import ChatOllama
from langchain.tools import Tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from ghosttown_mcp.clients.mcp_sync_client import MCPClientSync


client = MCPClientSync("http://localhost:4001/mcp/jsonrpc")


def add_via_sdk(a: float, b: float) -> float:
    """Add two numbers using the MCP-SDK client."""
    return client.call_tool("add_tool", a=a, b=b)


add_tool = Tool(
    name="add_tool",
    func=add_via_sdk,
    description="Add two numbers via MCP SDK/streamable HTTP"
)


if __name__ == "__main__":
    llm = ChatOllama(model="gpt-oss")

    # Set agent's policy to ensure it queries MCP server for arithmetic
    policy = (
        "You MUST use the provided tools from the MCP server for any arithmetic. "
        "Do not compute sums yourself. If no relevant tool exists, "
        "say you cannot proceed."
    )

    # Build a small ReAct agent graph with your tool
    app = create_react_agent(
        llm,
        [add_tool],
        prompt=policy,
        )

    # Invoke with a messages-style input (LangGraph standard)
    result = app.invoke({"messages": [HumanMessage(content="What is 123 + 456?")]})

    # The latest assistant message is at the end
    print(result["messages"][-1].content)

