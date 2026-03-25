"""
SauceDemo end-to-end flow tests using Page Object Model.
"""

from __future__ import annotations

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.saucedemo_login_page import SauceDemoLoginPage


BASE_URL = "https://www.saucedemo.com"
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.mark.regression
def test_invalid_login_shows_error_message(driver: WebDriver) -> None:
    # Step 1: Open SauceDemo login page.
    page = SauceDemoLoginPage(driver, BASE_URL)
    page.open()

    # Step 2: Try to log in with an invalid password.
    page.login(username=STANDARD_USER, password="wrong_password")

    # Step 3: Assert the expected login error is displayed.
    assert "Username and password do not match" in page.error_message()


@pytest.mark.regression
def test_add_to_cart_updates_badge_and_cart_contents(driver: WebDriver) -> None:
    # Step 1: Open SauceDemo and log in with a valid account.
    page = SauceDemoLoginPage(driver, BASE_URL)
    page.open()
    page.login(username=STANDARD_USER, password=PASSWORD)
    assert page.is_inventory_loaded(), "Inventory page did not load after login."

    # Step 2: Add one product to cart from inventory.
    page.add_backpack_to_cart()

    # Step 3: Assert cart badge updates to 1.
    assert page.cart_count() == 1, "Cart badge count should be 1 after adding one item."

    # Step 4: Open cart and assert the selected product is present.
    page.open_cart()
    assert page.first_cart_item_name() == "Sauce Labs Backpack"


@pytest.mark.e2e
def test_checkout_completes_successfully(driver: WebDriver) -> None:
    # Step 1: Open SauceDemo and log in.
    page = SauceDemoLoginPage(driver, BASE_URL)
    page.open()
    page.login(username=STANDARD_USER, password=PASSWORD)
    assert page.is_inventory_loaded(), "Inventory page did not load after login."

    # Step 2: Add item to cart and open cart page.
    page.add_backpack_to_cart()
    page.open_cart()
    assert page.first_cart_item_name() == "Sauce Labs Backpack"

    # Step 3: Start checkout and submit customer information.
    page.start_checkout()
    page.fill_checkout_information(
        first_name="Alan",
        last_name="QA",
        postal_code="12345",
    )

    # Step 4: Finish checkout and verify success confirmation.
    page.finish_checkout()
    assert page.checkout_complete_message() == "Thank you for your order!"


@pytest.mark.regression
def test_logout_returns_user_to_login_page(driver: WebDriver) -> None:
    # Step 1: Open SauceDemo and log in.
    page = SauceDemoLoginPage(driver, BASE_URL)
    page.open()
    page.login(username=STANDARD_USER, password=PASSWORD)
    assert page.is_inventory_loaded(), "Inventory page did not load after login."

    # Step 2: Log out from the burger menu.
    page.logout()

    # Step 3: Assert user is returned to login page.
    assert page.is_login_page_loaded(), "Login page did not load after logout."
    assert "saucedemo.com" in driver.current_url
