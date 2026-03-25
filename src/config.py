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


def _is_ci() -> bool:
    """True when running in CI (e.g. GitHub Actions sets CI=true)."""
    return _env("CI", "").lower() in ("1", "true", "yes")


def default_explicit_wait_seconds() -> float:
    """
    Default timeout for WebDriverWait in page objects.

    Override with env EXPLICIT_WAIT. CI runs use a higher default unless set.
    """
    raw = os.environ.get("EXPLICIT_WAIT")
    if raw and raw.strip():
        return float(raw.strip())
    return 25.0 if _is_ci() else 20.0


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
        IMPLICIT_WAIT — seconds (default: 15 local, 20 when CI=true)
        PAGE_LOAD_TIMEOUT — seconds (default: 60 local, 90 when CI=true)
        EXPLICIT_WAIT — WebDriverWait default in BasePage (default: 20 local, 25 CI)
        HEADLESS — true | false (default: false)
        WINDOW_WIDTH — pixels (default: 1280)
        WINDOW_HEIGHT — pixels (default: 720)
    """
    browser_raw = _env("BROWSER", "chrome").lower()
    if browser_raw not in ("chrome", "firefox", "edge"):
        browser_raw = "chrome"

    headless = _env("HEADLESS", "false").lower() in ("1", "true", "yes")

    implicit_default = "20" if _is_ci() else "15"
    page_load_default = "90" if _is_ci() else "60"

    return Settings(
        base_url=_env("BASE_URL", "https://example.com").rstrip("/"),
        browser=browser_raw,  # type: ignore[arg-type]
        implicit_wait_seconds=float(_env("IMPLICIT_WAIT", implicit_default)),
        page_load_timeout_seconds=float(_env("PAGE_LOAD_TIMEOUT", page_load_default)),
        headless=headless,
        window_width=int(_env("WINDOW_WIDTH", "1280")),
        window_height=int(_env("WINDOW_HEIGHT", "720")),
    )
