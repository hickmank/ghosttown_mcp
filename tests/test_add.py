"""Test for Ghost Town addition functionality."""

from ghosttown_mcp.tools.addition import add


def test_add() -> None:
    """Test the add function with positive and negative integers."""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
