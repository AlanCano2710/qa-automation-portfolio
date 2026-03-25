"""
Explicit wait helpers beyond BasePage (e.g. custom conditions).
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import default_explicit_wait_seconds


def wait_for_url_contains(
    driver: WebDriver, fragment: str, timeout: float | None = None
) -> None:
    """Assert URL contains a substring after navigation or redirect."""
    wait = timeout if timeout is not None else default_explicit_wait_seconds()
    WebDriverWait(driver, wait).until(lambda d: fragment in d.current_url)


def wait_stale(element: WebElement, driver: WebDriver, timeout: float | None = None) -> None:
    """Wait until a reference to an element goes stale (DOM replaced)."""
    wait = timeout if timeout is not None else default_explicit_wait_seconds()
    WebDriverWait(driver, wait).until(EC.staleness_of(element))
