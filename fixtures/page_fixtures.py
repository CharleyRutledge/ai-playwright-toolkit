"""
Page Fixtures
Custom pytest fixtures for page objects.
"""

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
    Fixture to provide a page with authentication.
    This is a placeholder - implement your authentication logic.

    Args:
        page: Playwright page instance

    Returns:
        Authenticated page instance
    """
    # TODO: Implement authentication logic
    # Example: page.goto("/login")
    # page.fill("#username", "testuser")
    # page.fill("#password", "password")
    # page.click("button[type='submit']")
    return page
