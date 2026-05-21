"""
Scenario Fixtures
Pytest fixtures for declarative scenario-driven testing.
"""
import os
from typing import Dict, Generator, List

import pytest
from playwright.sync_api import Page

from utils.scenario_runner import Scenario, ScenarioRunner, get_scenario_ids, load_scenarios


def _filter_scenario_ids() -> List[str]:
    """Resolve which scenarios to run from env or CLI."""
    single = os.environ.get("SCENARIO_ID")
    if single:
        return [single]
    mark = os.environ.get("SCENARIO_MARK")
    return get_scenario_ids(filter_mark=mark)


@pytest.fixture(scope="session")
def all_scenarios() -> Dict[str, Scenario]:
    """Load all scenarios from YAML once per session."""
    return load_scenarios()


@pytest.fixture
def scenario(request, all_scenarios: Dict[str, Scenario]) -> Scenario:
    """Provide the current parametrized scenario."""
    scenario_id = request.param
    if scenario_id not in all_scenarios:
        pytest.skip(f"Scenario '{scenario_id}' not found in data/scenarios.yaml")
    return all_scenarios[scenario_id]


@pytest.fixture
def scenario_page(page: Page, scenario: Scenario) -> Generator[Page, None, None]:
    """Page configured with scenario base URL context."""
    page.set_default_timeout(30000)
    yield page


@pytest.fixture
def scenario_runner(scenario_page: Page, scenario: Scenario) -> ScenarioRunner:
    """Runner bound to the current scenario."""
    return ScenarioRunner(scenario_page, scenario.base_url)
