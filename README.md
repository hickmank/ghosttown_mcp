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
|           ├── __init__.py
│           └── main.py
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

## 3. To build container and start MCP server locally

```
>> docker build -t ghosttown_mcp .
>> docker run --rm -p 4000:4000 ghosttown_mcp
```

## 4. To run the example client queries

```
>> python examples/raw_client.py
(WARNING!!!! CURRENTLY BROKEN)>> python examples/sdk_client.py
```
