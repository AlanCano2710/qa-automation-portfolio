"""
WebDriver factory: consistent browser setup for local and CI runs.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from src.config import BrowserName, Settings


def build_driver(settings: Settings) -> WebDriver:
    """
    Create a configured WebDriver for the requested browser.

    Uses webdriver-manager to resolve drivers compatible with the installed browser.
    """
    browser: BrowserName = settings.browser

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        # Shared-memory stability on Linux CI / Docker (GitHub Actions)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if settings.headless:
            options.add_argument("-headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:  # edge
        options = webdriver.EdgeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    driver.set_window_size(settings.window_width, settings.window_height)
    driver.implicitly_wait(settings.implicit_wait_seconds)
    driver.set_page_load_timeout(settings.page_load_timeout_seconds)

    return driver
