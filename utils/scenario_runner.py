"""
Scenario Runner
Execute declarative test scenarios from YAML configuration for any target site.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from playwright.sync_api import Page, expect


@dataclass
class ScenarioStep:
    """Single step in a test scenario."""

    action: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Scenario:
    """Declarative test scenario definition."""

    id: str
    name: str
    base_url: str
    steps: List[ScenarioStep]
    description: str = ""
    marks: List[str] = field(default_factory=list)


def load_scenarios(file_path: str = "data/scenarios.yaml") -> Dict[str, Scenario]:
    """
    Load scenarios from YAML file.

    Args:
        file_path: Path to scenarios YAML file

    Returns:
        Dictionary mapping scenario id to Scenario objects
    """
    path = Path(file_path)
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    scenarios: Dict[str, Scenario] = {}
    for scenario_id, config in (raw.get("scenarios") or {}).items():
        steps = [
            ScenarioStep(
                action=step["action"],
                params={k: v for k, v in step.items() if k != "action"},
            )
            for step in config.get("steps", [])
        ]
        scenarios[scenario_id] = Scenario(
            id=scenario_id,
            name=config.get("name", scenario_id),
            description=config.get("description", ""),
            base_url=config["base_url"],
            marks=config.get("marks", []),
            steps=steps,
        )
    return scenarios


def get_scenario_ids(
    file_path: str = "data/scenarios.yaml",
    filter_mark: Optional[str] = None,
) -> List[str]:
    """
    Get scenario ids, optionally filtered by pytest mark.

    Args:
        file_path: Path to scenarios YAML file
        filter_mark: Only return scenarios with this mark

    Returns:
        List of scenario ids
    """
    scenarios = load_scenarios(file_path)
    if filter_mark is None:
        return list(scenarios.keys())
    return [sid for sid, scenario in scenarios.items() if filter_mark in scenario.marks]


class ScenarioRunner:
    """Execute scenario steps against a Playwright page."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def run(self, scenario: Scenario) -> None:
        """Run all steps in a scenario."""
        for step in scenario.steps:
            self._execute_step(step)

    def _resolve_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        if url.startswith("/"):
            return f"{self.base_url}{url}"
        return f"{self.base_url}/{url}"

    def _execute_step(self, step: ScenarioStep) -> None:
        action = step.action
        params = step.params

        if action == "goto":
            self.page.goto(self._resolve_url(params["url"]))
            return

        if action == "reload":
            self.page.reload()
            if params.get("wait_until"):
                self.page.wait_for_load_state(params["wait_until"])
            return

        if action == "set_viewport":
            self.page.set_viewport_size(
                {"width": params["width"], "height": params["height"]}
            )
            return

        if action == "click_role":
            locator = self.page.get_by_role(params["role"], name=params["name"])
            if params.get("exact") is not None:
                locator = self.page.get_by_role(
                    params["role"], name=params["name"], exact=params["exact"]
                )
            if params.get("navigation"):
                with self.page.expect_navigation():
                    locator.click()
            else:
                locator.click()
            return

        if action == "click_link":
            locator = self.page.get_by_role("link", name=params["name"])
            if params.get("navigation"):
                with self.page.expect_navigation():
                    locator.click()
            else:
                locator.click()
            return

        if action == "fill_role":
            self.page.get_by_role(params["role"], name=params["name"]).fill(
                params["value"]
            )
            return

        if action == "fill_label":
            self.page.get_by_label(params["label"]).fill(params["value"])
            return

        if action == "hover_role":
            self.page.get_by_role(params["role"], name=params["name"]).hover()
            return

        if action == "press_key":
            self.page.keyboard.press(params["key"])
            return

        if action == "wait_for_load_state":
            self.page.wait_for_load_state(params.get("state", "load"))
            return

        if action == "screenshot":
            path = params.get("path", f"test-results/scenario_{action}.png")
            self.page.screenshot(path=path)
            return

        if action == "expect_title":
            expect(self.page).to_have_title(params["value"])
            return

        if action == "expect_title_contains":
            expect(self.page).to_have_title(re.compile(re.escape(params["text"])))
            return

        if action == "expect_url":
            expect(self.page).to_have_url(params["url"])
            return

        if action == "expect_url_contains":
            expect(self.page).to_have_url(re.compile(params["pattern"]))
            return

        if action == "expect_visible_role":
            expect(
                self.page.get_by_role(params["role"], name=params["name"])
            ).to_be_visible()
            return

        if action == "expect_visible_text":
            expect(self.page.get_by_text(params["text"])).to_be_visible()
            return

        if action == "expect_heading":
            locator = self.page.get_by_role(
                "heading", name=params["name"], exact=params.get("exact", True)
            )
            expect(locator).to_be_visible()
            if params.get("contains"):
                expect(locator).to_contain_text(params["contains"])
            return

        if action == "expect_heading_contains":
            expect(self.page.locator("h1")).to_contain_text(params["text"])
            return

        if action == "expect_body_visible":
            expect(self.page.locator("body")).to_be_visible()
            return

        if action == "expect_link":
            link = self.page.get_by_role("link", name=params["name"])
            expect(link).to_be_visible()
            if "href" in params:
                expect(link).to_have_attribute("href", params["href"])
            return

        if action == "expect_role_count":
            expect(self.page.get_by_role(params["role"])).to_have_count(
                params["count"]
            )
            return

        if action == "expect_element_count":
            expect(self.page.locator(params["selector"])).to_have_count(
                params["count"]
            )
            return

        if action == "expect_value_role":
            expect(
                self.page.get_by_role(params["role"], name=params["name"])
            ).to_have_value(params["value"])
            return

        if action == "evaluate_assert":
            result = self.page.evaluate(params["expression"])
            assert result == params["expected"], (
                f"Expected {params['expected']}, got {result}"
            )
            return

        if action == "performance_assert":
            start = self.page.evaluate("performance.now()")
            self.page.reload()
            self.page.wait_for_load_state(params.get("wait_until", "networkidle"))
            elapsed = self.page.evaluate("performance.now()") - start
            max_ms = params.get("max_ms", 5000)
            assert elapsed < max_ms, f"Load time {elapsed}ms exceeds {max_ms}ms"
            return

        raise ValueError(f"Unknown scenario action: {action}")
