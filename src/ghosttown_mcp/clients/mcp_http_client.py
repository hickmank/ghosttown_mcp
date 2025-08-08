"""Simple JSON-RPC raw client to interact with an MCP server."""

import requests
from typing import Any


class MCPHttpClient:
    """Synchronous JSON-RPC client for an MCP server over plain HTTP."""

    def __init__(self, url: str) -> None:
        """Initialize the HTTP client.

        Args:
            url (str): The MCP server's JSON-RPC endpoint,
                e.g. "http://localhost:4001/jsonrpc".
        """
        self.url = url

    def call_tool(
        self,
        method: str,
        params: dict[str, Any],
        request_id: int = 1
    ) -> Any:
        """Invoke a JSON-RPC method and return its result.

        Sends a single JSON-RPC request over HTTP POST and parses the response.

        Args:
            method (str): Name of the RPC method (e.g. "add_tool").
            params (Dict[str, Any]): Parameters for the method.
            request_id (int, optional): JSON-RPC message ID. Defaults to 1.

        Returns:
            Any: The value of the "result" field from the JSON-RPC response.

        Raises:
            RuntimeError: If the RPC response contains an "error" object.
            HTTPError: If the HTTP request itself fails (4xx/5xx).
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id,
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            err = data["error"]
            code = err.get("code")
            message = err.get("message")
            raise RuntimeError(f"RPC Error {code}: {message}")

        return data["result"]
