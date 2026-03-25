"""
Explicit wait helpers beyond BasePage (e.g. custom conditions).
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_url_contains(driver: WebDriver, fragment: str, timeout: float = 10) -> None:
    """Assert URL contains a substring after navigation or redirect."""
    WebDriverWait(driver, timeout).until(lambda d: fragment in d.current_url)


def wait_stale(element: WebElement, driver: WebDriver, timeout: float = 10) -> None:
    """Wait until a reference to an element goes stale (DOM replaced)."""
    WebDriverWait(driver, timeout).until(EC.staleness_of(element))
