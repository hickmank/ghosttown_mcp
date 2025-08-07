"""First simple MCP server based on JSON-RPC."""

from fastapi import FastAPI, Request
from fastapi.responses import Response
from jsonrpcserver import Success
from jsonrpcserver import method, dispatch

from ghosttown_mcp.tools.addition import add


app = FastAPI()


@method(name="add_tool")
def add_tool(a: float, b: float) -> float:
    """Add two floating point numbers using the add tool.

    Args:
    a (float): The first number to add.
    b (float): The second number to add.

    Returns:
        Result (JSONResponse): The sum of a and b wrapped in a JSON-RPC `success`
                               response.
    """
    return Success(add(a, b))


@app.post("/jsonrpc")
async def rpc_endpoint(request: Request) -> Response:
    """Handle JSON-RPC requests sent to the /jsonrpc endpoint.

    Args:
        request (Request): The incoming HTTP request containing the JSON-RPC payload.

    Returns:
        response (Response): The JSON-RPC response object.
    """
    request_text = await request.body()
    rpc_response = dispatch(request_text.decode())

    return Response(content=rpc_response, media_type="application/json")

