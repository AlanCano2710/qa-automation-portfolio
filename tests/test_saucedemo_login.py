"""
Real login test for https://www.saucedemo.com using Selenium + pytest.
"""

from __future__ import annotations

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.saucedemo_login_page import SauceDemoLoginPage


@pytest.mark.smoke
def test_standard_user_can_open_inventory_page(driver: WebDriver) -> None:
    # Step 1: Open the SauceDemo login page in the browser.
    page = SauceDemoLoginPage(driver, "https://www.saucedemo.com")
    page.open()

    # Step 2: Log in with a valid standard user account.
    page.login(username="standard_user", password="secret_sauce")

    # Step 3: Verify the inventory page loads after successful login.
    assert page.is_inventory_loaded(), "Inventory page did not load after login."
