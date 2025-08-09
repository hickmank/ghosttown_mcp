"""ReAct agent using LangGraph + Ollama that calls your JSON-RPC MCP tool."""

from langchain_ollama import ChatOllama
from langchain.tools import Tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from ghosttown_mcp.clients.mcp_http_client import MCPHttpClient

# Point to your plain JSON-RPC server
client = MCPHttpClient("http://localhost:4000/jsonrpc")


def add_via_http(a: float, b: float) -> float:
    """Add two numbers using the MCP HTTP client."""
    return client.call_tool("add_tool", {"a": a, "b": b})


# Wrap as a LangChain Tool (LangGraph accepts these)
add_tool = Tool(
    name="add",
    func=add_via_http,
    description="Add two numbers via plain JSON-RPC"
)


if __name__ == "__main__":
    llm = ChatOllama(model="gpt-oss")

    # Build a small ReAct agent graph with your tool
    app = create_react_agent(llm, [add_tool])

    # Invoke with a messages-style input (LangGraph standard)
    result = app.invoke({"messages": [HumanMessage(content="What is 123 + 456?")]})

    # The latest assistant message is at the end
    print(result["messages"][-1].content)







