"""ReAct agent using LangGraph + Ollama that calls your JSON-RPC MCP tool."""

from langchain_ollama import ChatOllama
from langchain.tools import Tool
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState

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
    description=("Add two numbers via plain JSON-RPC. "
                 "ALWAYS use this tool for arithmetic, do not compute sums yourself."),
)


if __name__ == "__main__":
    # Initialize the LLM client (Ollama)
    llm = ChatOllama(
        model="gpt-oss",
        #temperature=0.0,
        )

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
        #prompt=policy,
        )

    # Invoke with a messages-style input (LangGraph standard)
    result = app.invoke({"messages": [HumanMessage(content="What is 123 + 456?")]})

    # The latest assistant message is at the end
    print(result["messages"][-1].content)
