"""Example of LLM agent interaction with JSON-RPC MCP server."""

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import Ollama

from examples.mcp_http_client import MCPHttpClient


client = MCPHttpClient("http://localhost:4000/jsonrpc")


def add_via_http(a: float, b: float) -> float:
    """Add two numbers using the MCP HTTP client."""
    return client.call_tool("add_tool", {"a": a, "b": b})


# Create agents tool from the MCP server's add_tool method
add_tool = Tool(
    name="add",
    func=add_via_http,
    description="Add two numbers via plain JSON-RPC"
)


if __name__ == "__main__":
    llm = Ollama(model="gpt-oss")
    agent = initialize_agent(
        tools=[add_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    print(agent.run("What is 123 + 456?"))
