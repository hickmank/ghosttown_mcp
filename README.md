# Ghost Town MCP

This repository is meant as a learning platform to set up a very simple, very sparse Model Context Protocol (MCP) server. The code here is mainly meant as a educational resource for the creator.

The repository demonstrates a minimal MCP server implementation in Python, exposing an `add` tool, along with a simple client to invoke it.

## 1. Directory Structure

```
ghosttown_mcp/
├── .gitignore
├── README.md
├── Dockerfile
├── pyproject.toml
│
├── src/
│   └── ghosttown_mcp/
│       ├── __init__.py
│       ├── tools/
│           ├── __init__.py
│       │   └── addition.py
│       └── server/
│           └── jsonrpc
|               ├── __init__.py
│               └── server.py
│           └── fastmcp
|               ├── __init__.py
│               └── server.py
│
├── examples/
│   |── sdk_client.py
│   └── raw_client.py
│
└── tests/
    └── test_add.py
```

## 2. To install in python virtual environment

```
(mcp_venv)>> pip install flit
(mcp_venv)>> cd <ghosttown_mcp_rootdir>
(mcp_venv)>> flit install --symlink --deps=all
```

## 3. To build container and start JSON-RPC MCP server locally

```
>> docker build -f Dockerfile.jsonrpc -t ghosttown_mcp_jsonrpc .
>> docker run --rm -p 4000:4000 ghosttown_mcp_jsonrpc
```

## 4. To run the example JSON-RPC client query

```
>> python examples/raw_client.py
```

## 5. To build the container and start FastMCP MCP server locally

```
>> docker build -f Dockerfile.fastmcp -t ghosttown_mcp_fastmcp .
>> docker run --rm -p 4001:4001 ghosttown_mcp_fastmcp
```

## 6. To run the example MCP SDK client query

```
>> python examples/sdk_client.py
```
