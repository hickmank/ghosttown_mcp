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

