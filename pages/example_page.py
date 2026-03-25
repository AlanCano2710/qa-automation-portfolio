"""
Example page object for https://example.com (stable public page for demos).

Replace or extend with your application’s real pages.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ExamplePage(BasePage):
    """Minimal page object: heading and document title."""

    path = "/"

    HEADING = (By.TAG_NAME, "h1")

    def heading_text(self) -> str:
        el = self.wait_visible(self.HEADING)
        return el.text.strip()

    def page_title(self) -> str:
        return self.driver.title
