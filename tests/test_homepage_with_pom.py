"""
Homepage Tests Using Page Object Model
Tests for Playwright homepage using the new POM structure.
"""
import pytest
import allure
from playwright.sync_api import Page, expect
from page_objects.playwright_home_page import PlaywrightHomePage
from fixtures.page_fixtures import playwright_home_page


class TestHomepageWithPOM:
    """Test class for homepage using Page Object Model."""
    
    @pytest.mark.smoke
    @allure.title("Homepage Navigation with POM")
    @allure.description("Test basic navigation to Playwright website using Page Object Model")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Homepage")
    @allure.story("Navigation")
    @allure.label("test-type", "smoke")
    @allure.label("pattern", "page-object-model")
    def test_homepage_navigation_pom(self, page: Page):
        """Test homepage navigation using Page Object Model."""
        # Arrange
        home_page = PlaywrightHomePage(page)
        
        # Act
        home_page.navigate_to_home()
        
        # Assert
        expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")
        expect(home_page.main_heading).to_contain_text("web automation")
    
    @pytest.mark.regression
    @allure.title("Search Functionality with POM")
    @allure.description("Test search functionality using Page Object Model")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Search")
    @allure.story("Search Functionality")
    @allure.label("test-type", "regression")
    @allure.label("pattern", "page-object-model")
    def test_search_functionality_pom(self, page: Page):
        """Test search functionality using Page Object Model."""
        # Arrange
        home_page = PlaywrightHomePage(page)
        search_query = "python"
        
        # Act
        home_page.navigate_to_home()
        home_page.search(search_query)
        
        # Assert
        expect(home_page.search_box).to_have_value(search_query)
        expect(home_page.search_box).to_be_visible()
    
    @pytest.mark.regression
    @allure.title("Documentation Navigation with POM")
    @allure.description("Test navigation to documentation page using Page Object Model")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Navigation")
    @allure.story("Documentation Navigation")
    @allure.label("test-type", "regression")
    @allure.label("pattern", "page-object-model")
    def test_docs_navigation_pom(self, page: Page):
        """Test documentation navigation using Page Object Model."""
        # Arrange
        home_page = PlaywrightHomePage(page)
        
        # Act
        home_page.navigate_to_home()
        home_page.go_to_docs()
        
        # Assert
        expect(page).to_have_url("https://playwright.dev/docs/intro")
        expect(page.locator("h1")).to_contain_text("Installation")
    
    @pytest.mark.smoke
    @allure.title("Multiple Search Queries with POM")
    @allure.description("Test multiple search queries using Page Object Model")
    @allure.severity(allure.severity_level.MINOR)
    @allure.epic("Playwright Testing")
    @allure.feature("Search")
    @allure.story("Multiple Searches")
    @allure.label("test-type", "smoke")
    @allure.label("pattern", "page-object-model")
    @pytest.mark.parametrize("search_query", ["python", "javascript", "typescript", "locators"])
    def test_multiple_searches_pom(self, page: Page, search_query: str):
        """Test multiple search queries using Page Object Model."""
        # Arrange
        home_page = PlaywrightHomePage(page)
        
        # Act
        home_page.navigate_to_home()
        home_page.search(search_query)
        
        # Assert
        expect(home_page.search_box).to_have_value(search_query)

