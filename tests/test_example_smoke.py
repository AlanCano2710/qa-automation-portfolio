"""
Smoke tests against the configured BASE_URL (default: example.com).

These verify wiring: pytest, Selenium, Page Objects, and WebDriver setup.
"""

from __future__ import annotations

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.example_page import ExamplePage
from src.config import Settings


@pytest.mark.smoke
def test_example_page_heading(driver: WebDriver, settings: Settings) -> None:
    page = ExamplePage(driver, settings.base_url)
    page.open()
    assert page.heading_text() == "Example Domain"


@pytest.mark.smoke
def test_example_page_title(driver: WebDriver, settings: Settings) -> None:
    page = ExamplePage(driver, settings.base_url)
    page.open()
    assert page.page_title() == "Example Domain"
