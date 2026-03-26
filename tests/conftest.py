"""
Pytest fixtures shared across tests.

`driver` is function-scoped: one browser per test for isolation.
`settings` loads once per session from environment (see `src.config`).
Failed tests automatically capture full-page screenshots (Chromium) to
`reports/screenshots/`, named by test and timestamp.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.config import Settings, load_settings
from utils.driver_factory import build_driver
from utils.screenshot_helpers import sanitize_filename, save_failure_screenshot


REPORTS_DIR = Path("reports")
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Session-wide configuration."""
    return load_settings()


@pytest.fixture(scope="session", autouse=True)
def ensure_reports_directories() -> None:
    """Create report folders once per test session."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def driver(settings: Settings, request: pytest.FixtureRequest) -> WebDriver:
    """
    Yields a WebDriver; quits the browser after each test.

    Best practice: capture a screenshot only when the test call fails.
    """
    drv = build_driver(settings)
    try:
        yield drv
    finally:
        rep_call = getattr(request.node, "rep_call", None)
        if rep_call and rep_call.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            node = request.node
            mod_path = getattr(node, "path", None)
            module_stem = Path(mod_path).stem if mod_path is not None else Path(str(node.fspath)).stem
            test_name = sanitize_filename(request.node.name)
            filename = f"{module_stem}__{test_name}__{timestamp}.png"
            screenshot_path = SCREENSHOTS_DIR / filename
            save_failure_screenshot(drv, screenshot_path)
        drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    """
    Attach phase reports to test items.

    This enables fixtures to inspect `rep_call.failed` after test execution.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
