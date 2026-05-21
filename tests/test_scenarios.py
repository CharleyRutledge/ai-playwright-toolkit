"""
Scenario-Driven Tests
Run declarative scenarios from data/scenarios.yaml for any target site.
"""

import os

import allure
import pytest
from playwright.sync_api import Page

from fixtures.scenario_fixtures import _filter_scenario_ids
from utils.scenario_runner import Scenario, ScenarioRunner


def _scenario_id_list() -> list:
    ids = _filter_scenario_ids()
    return ids or ["playwright_smoke"]


@pytest.mark.scenario
@allure.epic("Scenario-Driven Testing")
@allure.feature("Declarative Scenarios")
class TestDeclarativeScenarios:
    """Execute YAML-defined scenarios for any website or user flow."""

    @pytest.mark.parametrize("scenario", _scenario_id_list(), indirect=True)
    def test_run_scenario(
        self,
        scenario: Scenario,
        scenario_runner: ScenarioRunner,
        scenario_page: Page,
    ) -> None:
        """Execute all steps defined for the scenario."""
        allure.dynamic.title(f"Scenario: {scenario.name}")
        allure.dynamic.description(scenario.description or scenario.id)
        allure.dynamic.label("scenario_id", scenario.id)
        allure.dynamic.label("base_url", scenario.base_url)

        with allure.step(f"Run scenario '{scenario.id}' ({len(scenario.steps)} steps)"):
            scenario_runner.run(scenario)

        assert scenario_page.url.startswith("http")
