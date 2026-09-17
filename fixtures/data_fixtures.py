"""
Data Fixtures
Custom pytest fixtures for test data.
"""

import pytest
from typing import Dict, Any
from utils.helpers import load_json
from pathlib import Path


@pytest.fixture
def test_data() -> Dict[str, Any]:
    """
    Fixture to provide test data.

    Returns:
        Dictionary of test data
    """
    return {
        "search_queries": ["python", "javascript", "typescript"],
        "valid_urls": ["/", "/docs/intro", "/community/welcome"],
        "test_user": {"username": "testuser", "email": "test@example.com"},
    }


@pytest.fixture
def json_test_data() -> Dict[str, Any]:
    """
    Fixture to load test data from JSON file.

    Returns:
        Dictionary of test data from JSON
    """
    data_file = Path("data/test_data.json")
    if data_file.exists():
        return load_json(str(data_file))
    return {}


@pytest.fixture
def api_test_data() -> Dict[str, Any]:
    """
    Fixture to provide API test data.

    Returns:
        Dictionary of API test data
    """
    return {
        "base_url": "https://api.example.com",
        "endpoints": {"users": "/users", "posts": "/posts", "comments": "/comments"},
        "headers": {"Content-Type": "application/json", "Accept": "application/json"},
    }
