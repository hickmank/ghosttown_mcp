"""First simple MCP server."""

from fastapi import FastAPI, Request
from fastapi.responses import Response
from jsonrpcserver import Success
from jsonrpcserver import method, dispatch
from sse_starlette.sse import EventSourceResponse

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


# 1) Initialization handshake
@method(name="initialize")
def initialize(protocolVersion: str, capabilities: dict, clientInfo: dict) -> Success:
    """Handle the initialization handshake for the MCP server.

    Args:
        protocolVersion (str): The protocol version from the client.
        capabilities (dict): The capabilities provided by the client.
        clientInfo (dict): Information about the client.

    Returns:
        Success: JSON-RPC success response containing server protocol and info.
    """
    return Success({
        "protocolVersion": "2025-03-26",
        "capabilities": {
            "tools": {"listChanged": False}
        },
        "serverInfo": {"name": "ghosttown_mcp", "version": "0.1.0"}
    })


# 2) Client’s “initialized” notification (no response needed)
@method(name="notifications/initialized")
def initialized() -> None:
    """Handle the client's 'initialized' notification.

    This function does not require any parameters and does not return a response.
    """
    return None


# 3) List available tools
@method(name="tools/list")
def list_tools() -> Success:
    """List all available tools provided by the MCP server.

    Returns:
        Success: JSON-RPC success response containing a list of available tools.
    """
    return Success([
        {"name": "add_tool", "description": "Add two numbers"}
    ])


# 4) Call a tool by name
@method(name="tools/call")
def call_tool(name: str, arguments: dict) -> Success:
    """Call a tool by its name with the provided arguments.

    Args:
        name (str): The name of the tool to call.
        arguments (dict): The arguments to pass to the tool.

    Returns:
        Success: JSON-RPC success response containing the result of the tool call.

    Raises:
        Exception: If the tool name is unknown.
    """
    if name != "add_tool":
        raise Exception(f"Unknown tool: {name}")

    result = add(arguments["a"], arguments["b"])
    # <-- Here we return an OBJECT, not a raw primitive,
    #     matching what the SDK expects: a dict with both
    #     'content' (list of TextContent blocks) and
    #     'structuredContent' (the raw value).
    return Success({
        # a list of text blocks for human‑readable fallback
        "content": [{"type": "text", "text": str(result)}],
        # structuredContent for programs to consume directly
        "structuredContent": {"value": result}
    })


@app.post("/jsonrpc")
async def rpc_endpoint(request: Request) -> Response:
    """Handle JSON-RPC requests sent to the /jsonrpc endpoint.

    Args:
        request (Request): The incoming HTTP request containing the JSON-RPC payload.

    Returns:
        response (Response): The JSON-RPC response object.
    """
    request_text = await request.body()
    rpc_response: str = dispatch(request_text.decode())

    accept = request.headers.get("accept", "")
    # SDK’s streamablehttp_client sends Accept: text/event-stream
    if "text/event-stream" in accept:
        async def event_gen():
            """Yield a single SSE event carrying our JSON-RPC reply."""
            yield rpc_response
        return EventSourceResponse(event_gen())

    return Response(content=rpc_response, media_type="application/json")

