"""
Failure screenshots: prefer full-page PNG on Chromium (Chrome / Edge) via CDP.
"""

from __future__ import annotations

import base64
import re
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver


def sanitize_filename(name: str, max_len: int = 150) -> str:
    """Make a string safe for use as a single path component."""
    s = re.sub(r"[^\w\-.]+", "_", name)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len] if s else "test"


def _chromium_full_page_png(driver: WebDriver) -> bytes | None:
    """
    Full-page screenshot using Chrome DevTools Protocol (Chromium-based drivers).

    Returns None if CDP is unavailable or capture fails (caller may fall back).
    """
    if not hasattr(driver, "execute_cdp_cmd"):
        return None
    try:
        result = driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "format": "png",
                "captureBeyondViewport": True,
                "fromSurface": True,
            },
        )
        data = result.get("data")
        if not data:
            return None
        return base64.b64decode(data)
    except Exception:
        return None


def save_failure_screenshot(driver: WebDriver, path: Path) -> None:
    """
    Save a PNG to ``path`` (parent dirs created as needed).

    Uses full-page capture on Chromium when possible; otherwise ``save_screenshot``
    (viewport only, e.g. Firefox).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    png = _chromium_full_page_png(driver)
    if png is not None:
        path.write_bytes(png)
    else:
        driver.save_screenshot(str(path))
