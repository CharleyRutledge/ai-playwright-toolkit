"""
Playwright Homepage Page Object
Contains locators and methods for Playwright's homepage.
"""
from playwright.sync_api import Page, Locator
from page_objects.base_page import BasePage


class PlaywrightHomePage(BasePage):
    """Page Object Model for Playwright homepage following official documentation patterns."""
    
    def __init__(self, page: Page):
        """
        Initialize Playwright homepage page object.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        # Define locators using accessibility-first approach
        self._search_button = None
        self._docs_link = None
        self._main_heading = None
        self._search_box = None
    
    @property
    def search_button(self) -> Locator:
        """Get search button locator."""
        if self._search_button is None:
            self._search_button = self.page.get_by_role("button", name="Search (Ctrl+K)")
        return self._search_button
    
    @property
    def docs_link(self) -> Locator:
        """Get docs link locator."""
        if self._docs_link is None:
            self._docs_link = self.page.get_by_role("link", name="Docs")
        return self._docs_link
    
    @property
    def main_heading(self) -> Locator:
        """Get main heading locator."""
        if self._main_heading is None:
            self._main_heading = self.page.locator("h1")
        return self._main_heading
    
    @property
    def search_box(self) -> Locator:
        """Get search box locator."""
        if self._search_box is None:
            self._search_box = self.page.get_by_role("searchbox", name="Search")
        return self._search_box
    
    def navigate_to_home(self):
        """Navigate to the Playwright homepage using base URL."""
        self.navigate("/")
    
    def search(self, query: str):
        """
        Perform a search on the website.
        
        Args:
            query: Search query text
        """
        # Click search button to open search
        self.search_button.click()
        # Wait for search box to be visible
        self.search_box.wait_for(state="visible")
        # Fill search query
        self.search_box.fill(query)
    
    def go_to_docs(self):
        """Navigate to the documentation page."""
        self.docs_link.click()

