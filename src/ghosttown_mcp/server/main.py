"""First simple MCP server."""

from fastapi import FastAPI, Request
from jsonrpcserver import method, async_dispatch
from ghosttown_mcp.tools.add import add


app = FastAPI()


@method
def add_tool(a: float, b: float) -> float:
    """Add two floating point numbers using the add tool.

    Args:
    a (float): The first number to add.
    b (float): The second number to add.

    Returns:
        sum (float): The sum of a and b.
    """
    return add(a, b)


@app.post("/jsonrpc")
async def rpc_endpoint(request: Request) -> object:
    """Handle JSON-RPC requests sent to the /jsonrpc endpoint.

    Args:
        request (Request): The incoming HTTP request containing the JSON-RPC payload.

    Returns:
        object: The JSON-RPC response object.
    """
    body = await request.body()
    return await async_dispatch(body.decode())
