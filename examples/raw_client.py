"""Client MCP interaction with direct JSON-RPC calls."""

import requests


RPC_URL = "http://localhost:4000/jsonrpc"


def rpc_call(method: str, params: dict, req_id: int = 1) -> object:
    """Make a JSON-RPC call to the MCP server.

    Args:
        method (str): The RPC method name to call.
        params (dict): The parameters to send with the RPC call.
        req_id (int, optional): The request ID for the RPC call (default is 1).

    Returns:
        object: The result returned by the RPC call.

    Raises:
        RuntimeError: If the RPC response contains an error.
    """
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": req_id}
    r = requests.post(RPC_URL, json=payload)
    r.raise_for_status()
    resp = r.json()
    if "error" in resp:
        raise RuntimeError(resp["error"])
    return resp["result"]


if __name__ == "__main__":
    print("4 + 5 =", rpc_call("add_tool", {"a": 4, "b": 5}))
