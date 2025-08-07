"""Server setup for the FastMCP based server."""

from mcp.server.fastmcp import FastMCP

# Create your MCP application instance
mcp = FastMCP(name="FastMCP Demo")

# Declare a tool with a simple decorator
@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    # Run an ASGI server on 0.0.0.0:4002
    mcp.run(host="0.0.0.0", port=4002)

