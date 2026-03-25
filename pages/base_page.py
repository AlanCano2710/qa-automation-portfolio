"""
Base page: shared Selenium helpers for all page objects.
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import default_explicit_wait_seconds


class BasePage:
    """
    Parent class for Page Objects.

    Subclasses set `path` (optional URL path relative to base URL) and define
    locators plus action methods.
    """

    path: str = ""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self._driver = driver
        self._base_url = base_url.rstrip("/")

    @property
    def driver(self) -> WebDriver:
        return self._driver

    def open(self) -> None:
        """Navigate to this page (base URL + path)."""
        url = f"{self._base_url}{self.path}" if self.path else self._base_url
        self._driver.get(url)

    def wait_visible(
        self, locator: tuple[str, str], timeout: float | None = None
    ) -> WebElement:
        """Wait until element is present and visible; return it."""
        wait = timeout if timeout is not None else default_explicit_wait_seconds()
        return WebDriverWait(self._driver, wait).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(
        self, locator: tuple[str, str], timeout: float | None = None
    ) -> WebElement:
        """Wait until element is clickable; return it."""
        wait = timeout if timeout is not None else default_explicit_wait_seconds()
        return WebDriverWait(self._driver, wait).until(
            EC.element_to_be_clickable(locator)
        )
