"""
Data-Driven Tests
Tests using data factories and fixtures.
"""
import pytest
import allure
from playwright.sync_api import Page, expect
from page_objects.playwright_home_page import PlaywrightHomePage
from data.factories import UserFactory, FormFactory
from utils.helpers import get_timestamp


class TestDataDriven:
    """Test class demonstrating data-driven testing."""
    
    @pytest.mark.regression
    @allure.title("Search with Test Data")
    @allure.description("Test search using data from JSON fixture")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Search")
    @allure.story("Data-Driven Testing")
    @allure.label("test-type", "regression")
    @allure.label("pattern", "data-driven")
    def test_search_with_test_data(self, page: Page, test_data):
        """Test search functionality using test data fixture."""
        # Arrange
        home_page = PlaywrightHomePage(page)
        search_queries = test_data.get("search_queries", ["python"])
        
        # Act & Assert for each query
        for query in search_queries:
            with allure.step(f"Search for: {query}"):
                home_page.navigate_to_home()
                home_page.search(query)
                expect(home_page.search_box).to_have_value(query)
                
                # Navigate back to home for next search
                page.keyboard.press("Escape")
    
    @pytest.mark.smoke
    @allure.title("Search with JSON Test Data")
    @allure.description("Test search using JSON test data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Search")
    @allure.story("Data-Driven Testing")
    @allure.label("test-type", "smoke")
    @allure.label("pattern", "data-driven")
    def test_search_with_json_data(self, page: Page, json_test_data):
        """Test search functionality using JSON test data."""
        if not json_test_data:
            pytest.skip("No JSON test data available")
        
        # Arrange
        home_page = PlaywrightHomePage(page)
        playwright_data = json_test_data.get("playwright_website", {})
        search_queries = playwright_data.get("search_queries", [])
        
        if not search_queries:
            pytest.skip("No search queries in test data")
        
        # Act & Assert
        for query in search_queries[:2]:  # Test first 2 queries
            with allure.step(f"Search for: {query}"):
                home_page.navigate_to_home()
                home_page.search(query)
                expect(home_page.search_box).to_have_value(query)
                page.keyboard.press("Escape")
    
    @pytest.mark.regression
    @allure.title("User Factory Demo")
    @allure.description("Demonstrate user factory usage")
    @allure.severity(allure.severity_level.MINOR)
    @allure.epic("Playwright Testing")
    @allure.feature("Data Factories")
    @allure.story("User Factory")
    @allure.label("test-type", "regression")
    @allure.label("pattern", "factory")
    def test_user_factory_demo(self):
        """Demonstrate user factory for generating test data."""
        # Create regular user
        user = UserFactory.create_user()
        assert user.username is not None
        assert user.email is not None
        assert user.role == "user"
        
        # Create admin user
        admin = UserFactory.create_admin_user()
        assert admin.role == "admin"
        
        # Create custom user
        custom_user = UserFactory.create_user(username="testuser", email="test@example.com")
        assert custom_user.username == "testuser"
        assert custom_user.email == "test@example.com"
        
        with allure.step("User data generated successfully"):
            allure.attach(
                f"User: {user.username}, Email: {user.email}",
                name="Generated User Data",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @pytest.mark.regression
    @allure.title("Form Factory Demo")
    @allure.description("Demonstrate form factory usage")
    @allure.severity(allure.severity_level.MINOR)
    @allure.epic("Playwright Testing")
    @allure.feature("Data Factories")
    @allure.story("Form Factory")
    @allure.label("test-type", "regression")
    @allure.label("pattern", "factory")
    def test_form_factory_demo(self):
        """Demonstrate form factory for generating form data."""
        # Create form data
        form_data = FormFactory.create_form_data()
        assert form_data.email is not None
        assert form_data.message is not None
        
        # Create invalid email form data
        invalid_form = FormFactory.create_invalid_email_data()
        assert invalid_form.email in ["notanemail", "@example.com", "test@", "test"]
        
        # Create custom form data
        custom_form = FormFactory.create_form_data(
            email="custom@example.com",
            message="Custom message",
            subject="Test Subject"
        )
        assert custom_form.email == "custom@example.com"
        assert custom_form.subject == "Test Subject"
        
        with allure.step("Form data generated successfully"):
            allure.attach(
                f"Email: {form_data.email}, Message: {form_data.message}",
                name="Generated Form Data",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @pytest.mark.smoke
    @allure.title("Timestamp Utility Demo")
    @allure.description("Demonstrate timestamp utility usage")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.epic("Playwright Testing")
    @allure.feature("Utilities")
    @allure.story("Helper Functions")
    @allure.label("test-type", "smoke")
    @allure.label("pattern", "utility")
    def test_timestamp_utility_demo(self):
        """Demonstrate timestamp utility for unique identifiers."""
        # Get timestamp
        timestamp = get_timestamp()
        assert timestamp is not None
        assert len(timestamp) > 0
        
        # Get custom format timestamp
        custom_timestamp = get_timestamp("%Y-%m-%d")
        assert "-" in custom_timestamp
        
        with allure.step("Timestamp generated successfully"):
            allure.attach(
                f"Default: {timestamp}, Custom: {custom_timestamp}",
                name="Generated Timestamps",
                attachment_type=allure.attachment_type.TEXT
            )

