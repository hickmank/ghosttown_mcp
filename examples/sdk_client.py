"""Simple MCP SDK client interaction."""

from mcp.client import MCPClient


def main() -> None:
    """Interact with the MCP SDK client.

    Invoke 'add_tool' method and print the result.
    """
    client = MCPClient(url="http://localhost:4000/jsonrpc")
    result = client.invoke("add_tool", {"a": 2, "b": 3})
    print("2 + 3 =", result)

if __name__ == "__main__":
    main()
