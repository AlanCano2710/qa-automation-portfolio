"""
Central configuration for tests.

Prefer environment variables for secrets and URLs that differ per environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal


BrowserName = Literal["chrome", "firefox", "edge"]


def _env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value.strip() if value else default


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings."""

    base_url: str
    browser: BrowserName
    implicit_wait_seconds: float
    page_load_timeout_seconds: float
    headless: bool
    window_width: int
    window_height: int


def load_settings() -> Settings:
    """
    Load settings from environment with safe defaults.

    Environment variables (all optional):
        BASE_URL — Application under test (default: https://example.com)
        BROWSER — chrome | firefox | edge (default: chrome)
        IMPLICIT_WAIT — seconds (default: 10)
        PAGE_LOAD_TIMEOUT — seconds (default: 30)
        HEADLESS — true | false (default: false)
        WINDOW_WIDTH — pixels (default: 1280)
        WINDOW_HEIGHT — pixels (default: 720)
    """
    browser_raw = _env("BROWSER", "chrome").lower()
    if browser_raw not in ("chrome", "firefox", "edge"):
        browser_raw = "chrome"

    headless = _env("HEADLESS", "false").lower() in ("1", "true", "yes")

    return Settings(
        base_url=_env("BASE_URL", "https://example.com").rstrip("/"),
        browser=browser_raw,  # type: ignore[arg-type]
        implicit_wait_seconds=float(_env("IMPLICIT_WAIT", "10")),
        page_load_timeout_seconds=float(_env("PAGE_LOAD_TIMEOUT", "30")),
        headless=headless,
        window_width=int(_env("WINDOW_WIDTH", "1280")),
        window_height=int(_env("WINDOW_HEIGHT", "720")),
    )
