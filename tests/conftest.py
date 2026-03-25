"""
Pytest fixtures shared across tests.

`driver` is function-scoped: one browser per test for isolation.
`settings` loads once per session from environment (see `src.config`).
"""

from __future__ import annotations

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.config import Settings, load_settings
from utils.driver_factory import build_driver


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Session-wide configuration."""
    return load_settings()


@pytest.fixture
def driver(settings: Settings) -> WebDriver:
    """
    Yields a WebDriver; quits the browser after each test.

    Use the `driver` fixture in tests that need a real browser.
    """
    drv = build_driver(settings)
    try:
        yield drv
    finally:
        drv.quit()
