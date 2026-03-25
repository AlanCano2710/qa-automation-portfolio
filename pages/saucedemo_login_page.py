"""
Page object for SauceDemo login and inventory verification.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SauceDemoLoginPage(BasePage):
    """Encapsulates login actions and post-login checks for SauceDemo."""

    path = "/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    INVENTORY_TITLE = (By.CSS_SELECTOR, ".title")

    def login(self, username: str, password: str) -> None:
        """Log in with supplied credentials."""
        self.wait_visible(self.USERNAME_INPUT).send_keys(username)
        self.wait_visible(self.PASSWORD_INPUT).send_keys(password)
        self.wait_clickable(self.LOGIN_BUTTON).click()

    def is_inventory_loaded(self) -> bool:
        """
        Returns True when the inventory page heading is visible.

        SauceDemo inventory page uses a title element with text: 'Products'.
        """
        return self.wait_visible(self.INVENTORY_TITLE).text.strip() == "Products"
