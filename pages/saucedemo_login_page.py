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
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_TITLE = (By.CSS_SELECTOR, ".title")
    ADD_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def login(self, username: str, password: str) -> None:
        """Log in with supplied credentials."""
        self.wait_visible(self.USERNAME_INPUT).send_keys(username)
        self.wait_visible(self.PASSWORD_INPUT).send_keys(password)
        self.wait_clickable(self.LOGIN_BUTTON).click()

    def error_message(self) -> str:
        """Return invalid-login error text."""
        return self.wait_visible(self.ERROR_MESSAGE).text.strip()

    def is_inventory_loaded(self) -> bool:
        """
        Returns True when the inventory page heading is visible.

        SauceDemo inventory page uses a title element with text: 'Products'.
        """
        return self.wait_visible(self.INVENTORY_TITLE).text.strip() == "Products"

    def add_backpack_to_cart(self) -> None:
        """Add Sauce Labs Backpack item from inventory page."""
        self.wait_clickable(self.ADD_BACKPACK_BUTTON).click()

    def cart_count(self) -> int:
        """Return numeric cart badge count."""
        return int(self.wait_visible(self.CART_BADGE).text.strip())

    def open_cart(self) -> None:
        """Open cart page from top-right cart icon."""
        self.wait_clickable(self.CART_LINK).click()

    def first_cart_item_name(self) -> str:
        """Return the first item name shown in cart."""
        return self.wait_visible(self.CART_ITEM_NAME).text.strip()

    def start_checkout(self) -> None:
        """Start checkout from cart page."""
        self.wait_clickable(self.CHECKOUT_BUTTON).click()

    def fill_checkout_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """Fill checkout customer information and continue."""
        self.wait_visible(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.wait_visible(self.LAST_NAME_INPUT).send_keys(last_name)
        self.wait_visible(self.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.wait_clickable(self.CONTINUE_BUTTON).click()

    def finish_checkout(self) -> None:
        """Complete checkout on overview page."""
        self.wait_clickable(self.FINISH_BUTTON).click()

    def checkout_complete_message(self) -> str:
        """Return checkout confirmation header text."""
        return self.wait_visible(self.COMPLETE_HEADER).text.strip()

    def logout(self) -> None:
        """Log out from the inventory menu."""
        self.wait_clickable(self.MENU_BUTTON).click()
        self.wait_clickable(self.LOGOUT_LINK, timeout=15).click()

    def is_login_page_loaded(self) -> bool:
        """Return True when login button is visible."""
        return self.wait_visible(self.LOGIN_BUTTON).is_displayed()
