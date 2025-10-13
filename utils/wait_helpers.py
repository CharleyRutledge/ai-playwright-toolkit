"""
Wait Helpers
Utility functions for waiting and synchronization.
"""
from playwright.sync_api import Page, Locator, expect
from typing import Callable


def wait_for_element_visible(locator: Locator, timeout: int = 30000):
    """
    Wait for element to be visible.
    
    Args:
        locator: Element locator
        timeout: Timeout in milliseconds
    """
    locator.wait_for(state="visible", timeout=timeout)


def wait_for_element_hidden(locator: Locator, timeout: int = 30000):
    """
    Wait for element to be hidden.
    
    Args:
        locator: Element locator
        timeout: Timeout in milliseconds
    """
    locator.wait_for(state="hidden", timeout=timeout)


def wait_for_url_change(page: Page, expected_url: str, timeout: int = 30000):
    """
    Wait for URL to change to expected value.
    
    Args:
        page: Playwright page instance
        expected_url: Expected URL
        timeout: Timeout in milliseconds
    """
    page.wait_for_url(expected_url, timeout=timeout)


def wait_for_load_state(page: Page, state: str = "load", timeout: int = 30000):
    """
    Wait for page to reach specific load state.
    
    Args:
        page: Playwright page instance
        state: Load state (load, domcontentloaded, networkidle)
        timeout: Timeout in milliseconds
    """
    page.wait_for_load_state(state, timeout=timeout)


def wait_for_condition(condition: Callable[[], bool], timeout: int = 30, interval: int = 1) -> bool:
    """
    Wait for custom condition to be true.
    
    Args:
        condition: Callable that returns boolean
        timeout: Timeout in seconds
        interval: Check interval in seconds
        
    Returns:
        True if condition met, False if timeout
    """
    import time
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        if condition():
            return True
        time.sleep(interval)
    
    return False

