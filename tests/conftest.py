import os
import sys
from datetime import datetime
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv(project_root / ".env")

DEFAULT_BASE_URL = os.environ.get("BASE_URL", "https://playwright.dev")

from fixtures.data_fixtures import *  # noqa: E402, F403
from fixtures.page_fixtures import *  # noqa: E402, F403
from fixtures.scenario_fixtures import *  # noqa: E402, F403


@pytest.fixture(scope="session", autouse=True)
def browser_context_args():
    """Browser context arguments for all tests."""
    test_results_dir = Path("test-results")
    test_results_dir.mkdir(exist_ok=True)

    context_args = {
        "base_url": DEFAULT_BASE_URL,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "extra_http_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
        "record_video_dir": str(test_results_dir / "videos"),
    }

    if os.environ.get("USE_STORAGE_STATE", "").lower() in ("1", "true", "yes"):
        context_args["storage_state"] = os.environ.get("STORAGE_STATE", "state.json")

    return context_args


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Browser launch arguments for all tests."""
    return {
        "headless": True,
        "slow_mo": 0,
    }


@pytest.fixture(scope="function")
def trace_test(page):
    """Enable tracing for individual tests."""
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield page
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
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            page = item.funcargs["page"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"test-results/screenshot_{item.name}_{timestamp}.png"
            page.screenshot(path=screenshot_path)

            with open(screenshot_path, "rb") as handle:
                allure.attach(
                    handle.read(),
                    name=f"Screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )

            content_path = f"test-results/page_content_{item.name}_{timestamp}.html"
            with open(content_path, "w", encoding="utf-8") as handle:
                handle.write(page.content())

            with open(content_path, "r", encoding="utf-8") as handle:
                allure.attach(
                    handle.read(),
                    name=f"Page_Content_{item.name}",
                    attachment_type=allure.attachment_type.HTML,
                )

            print("Screenshot and page content attached to Allure report")


@pytest.fixture(scope="function")
def allure_environment(request):
    """Set Allure environment information."""
    browser = request.config.getoption("--browser", default="chromium")
    allure.dynamic.environment(
        base_url=DEFAULT_BASE_URL,
        browser=browser,
        platform="linux",
        python_version=sys.version,
    )
