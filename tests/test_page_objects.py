import pytest
import allure
from playwright.sync_api import Page, expect


class PlaywrightHomePage:
    """Page Object Model for Playwright homepage following official documentation patterns."""

    def __init__(self, page: Page):
        self.page = page
        # Search button using role selector
        self.search_button = page.get_by_role("button", name="Search (Ctrl+K)")
        # Docs link using role selector
        self.docs_link = page.get_by_role("link", name="Docs")
        # Main heading for verification
        self.main_heading = page.locator("h1")
        # Search box for input
        self.search_box = page.get_by_role("searchbox", name="Search")

    def navigate(self):
        """Navigate to the Playwright homepage using base URL."""
        self.page.goto("/")

    def search(self, query: str):
        """Perform a search on the website."""
        # Click search button to open search
        self.search_button.click()
        # Wait for search box to be visible
        self.search_box.wait_for(state="visible")
        # Fill search query
        self.search_box.fill(query)

    def go_to_docs(self):
        """Navigate to the documentation page."""
        self.docs_link.click()


class TestPageObjectModel:
    """Test class demonstrating Page Object Model pattern."""

    @pytest.mark.smoke
    @allure.title("Homepage Page Object Test")
    @allure.description("Test using Page Object Model pattern with base URL")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Page Object Model")
    @allure.story("Homepage Navigation")
    @allure.label("test-type", "smoke")
    @allure.label("pattern", "page-object")
    def test_homepage_with_page_object(self, page: Page):
        """Test using Page Object Model pattern with base URL."""
        # Create page object instance
        home_page = PlaywrightHomePage(page)

        # Navigate to homepage using base URL
        home_page.navigate()

        # Verify page title
        expect(page).to_have_title(
            "Fast and reliable end-to-end testing for modern web apps | Playwright"
        )

        # Verify main heading is visible
        expect(home_page.main_heading).to_contain_text("web automation")

    @pytest.mark.regression
    @allure.title("Search Page Object Test")
    @allure.description("Test search functionality using Page Object Model with base URL")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Page Object Model")
    @allure.story("Search Functionality")
    @allure.label("test-type", "regression")
    @allure.label("pattern", "page-object")
    def test_search_with_page_object(self, page: Page):
        """Test search functionality using Page Object Model with base URL."""
        # Create page object instance
        home_page = PlaywrightHomePage(page)

        # Navigate to homepage using base URL
        home_page.navigate()

        # Perform search using page object method
        home_page.search("python")

        # Verify search box contains the entered text
        expect(home_page.search_box).to_have_value("python")

        # Verify that search functionality is working
        expect(home_page.search_box).to_be_visible()

    @pytest.mark.slow
    @allure.title("Documentation Navigation Page Object Test")
    @allure.description("Test documentation navigation using Page Object Model with base URL")
    @allure.severity(allure.severity_level.MINOR)
    @allure.epic("Playwright Testing")
    @allure.feature("Page Object Model")
    @allure.story("Documentation Navigation")
    @allure.label("test-type", "slow")
    @allure.label("pattern", "page-object")
    def test_docs_navigation_with_page_object(self, page: Page):
        """Test documentation navigation using Page Object Model with base URL."""
        # Create page object instance
        home_page = PlaywrightHomePage(page)

        # Navigate to homepage using base URL
        home_page.navigate()

        # Go to documentation using page object method
        home_page.go_to_docs()

        # Verify we're on docs page
        expect(page).to_have_url("https://playwright.dev/docs/intro")

        # Verify documentation content (actual heading is "Installation")
        expect(page.locator("h1")).to_contain_text("Installation")
