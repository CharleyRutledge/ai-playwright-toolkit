"""
Base Page Object
Provides common functionality for all page objects.
"""
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects with common functionality."""
    
    def __init__(self, page: Page):
        """
        Initialize base page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
    
    def navigate(self, url: str):
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to (can be relative or absolute)
        """
        self.page.goto(url)
    
    def get_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            Current page title
        """
        return self.page.title()
    
    def get_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            Current page URL
        """
        return self.page.url
    
    def wait_for_load_state(self, state: str = "load"):
        """
        Wait for page to reach a specific load state.
        
        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle)
        """
        self.page.wait_for_load_state(state)
    
    def take_screenshot(self, path: str):
        """
        Take a screenshot of the current page.
        
        Args:
            path: Path to save screenshot
        """
        self.page.screenshot(path=path)
    
    def verify_title(self, expected_title: str):
        """
        Verify the page title matches expected value.
        
        Args:
            expected_title: Expected page title
        """
        expect(self.page).to_have_title(expected_title)
    
    def verify_url(self, expected_url: str):
        """
        Verify the page URL matches expected value.
        
        Args:
            expected_url: Expected page URL
        """
        expect(self.page).to_have_url(expected_url)

