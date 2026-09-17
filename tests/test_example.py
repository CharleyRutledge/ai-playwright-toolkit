import pytest
import allure
from playwright.sync_api import Page, expect


class TestExample:
    """Example test class following Playwright's official documentation patterns."""

    @pytest.mark.smoke
    @allure.title("Basic Navigation Test")
    @allure.description("Test basic navigation to Playwright website using base URL")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Navigation")
    @allure.story("Basic Navigation")
    @allure.label("test-type", "smoke")
    def test_basic_navigation(self, page: Page):
        """Test basic navigation to Playwright website using base URL."""
        # Navigate to Playwright homepage using base URL
        page.goto("/")

        # Verify the page title contains Playwright
        expect(page).to_have_title(
            "Fast and reliable end-to-end testing for modern web apps | Playwright"
        )

        # Verify the main heading is visible
        expect(page.locator("h1")).to_contain_text("Playwright enables reliable end-to-end testing")

    @pytest.mark.regression
    @allure.title("Search Functionality Test")
    @allure.description("Test search functionality on Playwright website using base URL")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Search")
    @allure.story("Search Functionality")
    @allure.label("test-type", "regression")
    def test_search_functionality(self, page: Page):
        """Test search functionality on Playwright website using base URL."""
        # Navigate to the website using base URL
        page.goto("/")

        # Click on the search button using role selector
        page.get_by_role("button", name="Search (Ctrl+K)").click()

        # Wait for search box to be visible and type search query
        search_box = page.get_by_role("searchbox", name="Search")
        search_box.wait_for(state="visible")
        search_box.fill("python")

        # Verify search box contains the entered text
        expect(search_box).to_have_value("python")

        # Verify that search functionality is working by checking search box is active
        expect(search_box).to_be_visible()

    @pytest.mark.slow
    @allure.title("Documentation Navigation Test")
    @allure.description("Test navigation to documentation page using base URL")
    @allure.severity(allure.severity_level.MINOR)
    @allure.epic("Playwright Testing")
    @allure.feature("Navigation")
    @allure.story("Documentation Navigation")
    @allure.label("test-type", "slow")
    def test_documentation_navigation(self, page: Page):
        """Test navigation to documentation page using base URL."""
        # Navigate to the website using base URL
        page.goto("/")

        # Click on the Docs link in navigation
        page.get_by_role("link", name="Docs").click()

        # Verify we're on the documentation page
        expect(page).to_have_url("https://playwright.dev/docs/intro")

        # Verify documentation content is present (actual heading is "Installation")
        expect(page.locator("h1")).to_contain_text("Installation")
