"""
Page Fixtures
Custom pytest fixtures for page objects.
"""
import os
from pathlib import Path

import pytest
from playwright.sync_api import Page
from page_objects.playwright_home_page import PlaywrightHomePage


@pytest.fixture
def playwright_home_page(page: Page) -> PlaywrightHomePage:
    """
    Fixture to provide Playwright home page object.

    Args:
        page: Playwright page instance

    Returns:
        PlaywrightHomePage instance
    """
    return PlaywrightHomePage(page)


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    Fixture providing a page with persisted storage state for authenticated flows.

    Set USE_STORAGE_STATE=true and optionally STORAGE_STATE=path/to/state.json.
    Generate state with: playwright codegen --save-storage=state.json <login-url>
    """
    storage_path = os.environ.get("STORAGE_STATE", "state.json")
    if os.environ.get("USE_STORAGE_STATE", "").lower() in ("1", "true", "yes"):
        if Path(storage_path).exists():
            return page
        pytest.skip(f"Storage state file not found: {storage_path}")
    return page
