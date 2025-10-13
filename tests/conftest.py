import pytest
import os
import sys
import allure
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import custom fixtures
from fixtures.page_fixtures import *
from fixtures.data_fixtures import *


@pytest.fixture(scope="session", autouse=True)
def browser_context_args():
    """Browser context arguments for all tests following official Playwright documentation."""
    
    # Create test-results directory for Playwright recordings
    test_results_dir = Path("test-results")
    test_results_dir.mkdir(exist_ok=True)
    
    return {
        # Base URL to use in actions like page.goto('/')
        "base_url": "https://playwright.dev",
        
        # Viewport settings for all pages in the context
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        
        # Ignore HTTPS errors during navigation
        "ignore_https_errors": True,
        
        # Populates context with given storage state (for authentication)
        # "storage_state": "state.json",  # Uncomment when you have auth state
        
        # Additional HTTP headers to be sent with every request
        "extra_http_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
        
        # Playwright recording features
        "record_video_dir": str(test_results_dir / "videos"),  # Record videos of test runs
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Browser launch arguments for all tests following official Playwright documentation."""
    return {
        "headless": True,  # Set to True for headless mode
        "slow_mo": 0,      # No slow motion in headless mode
        # Additional launch options can be added here
        # "args": ["--disable-web-security"],
    }


@pytest.fixture(scope="session")
def browser_name():
    """Default browser for all tests."""
    return "chromium"  # Options: chromium, firefox, webkit


@pytest.fixture(scope="function")
def trace_test(page):
    """Enable tracing for individual tests."""
    # Start tracing
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield page
    
    # Stop tracing and save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_file = f"test-results/trace_{timestamp}.zip"
    page.context.tracing.stop(path=trace_file)
    print(f"Trace saved to: {trace_file}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure and attach to Allure report."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Take screenshot on test failure and attach to Allure
        if hasattr(item, 'funcargs') and 'page' in item.funcargs:
            page = item.funcargs['page']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"test-results/screenshot_{item.name}_{timestamp}.png"
            page.screenshot(path=screenshot_path)
            
            # Attach screenshot to Allure report
            with open(screenshot_path, 'rb') as f:
                allure.attach(f.read(), name=f"Screenshot_{item.name}", attachment_type=allure.attachment_type.PNG)
            
            # Also save page content for debugging
            content_path = f"test-results/page_content_{item.name}_{timestamp}.html"
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            
            # Attach page content to Allure report
            with open(content_path, 'r', encoding='utf-8') as f:
                allure.attach(f.read(), name=f"Page_Content_{item.name}", attachment_type=allure.attachment_type.HTML)
            
            print(f"Screenshot and page content attached to Allure report")


@pytest.fixture(scope="function")
def allure_environment():
    """Set Allure environment information."""
    allure.dynamic.environment(
        base_url="https://playwright.dev",
        browser="chromium",
        platform="Windows",
        python_version=os.sys.version
    ) 