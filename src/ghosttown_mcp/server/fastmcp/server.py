"""Server setup for the FastMCP based server."""

from fastmcp import FastMCP


# Create your MCP application instance
mcp = FastMCP(name="FastMCP Demo")

# Declare a tool with a simple decorator
@mcp.tool()
def add_tool(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

# Expose the Asynchronous Server Gateway Interface (ASGI) app for Uvicorn
#
# This mounts the MCP JSON-RPC (Streamable HTTP) endpoint under /mcp/
# by default (and /sse/ if you choose transport="sse").
app = mcp.http_app(path="/mcp", transport="http")

if __name__ == "__main__":
    # Run an ASGI server on 0.0.0.0:4001
    mcp.run(host="0.0.0.0", port=4001)

