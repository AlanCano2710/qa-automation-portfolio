"""
Page Object Model (POM) layer.

Each page class encapsulates locators and user-visible actions for one screen.
Tests should call page methods, not raw Selenium calls, to stay maintainable.
"""

from pages.base_page import BasePage

__all__ = ["BasePage"]
