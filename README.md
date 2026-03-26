# QA Automation Portfolio

[![Python Pytest CI](https://github.com/AlanCano2710/qa-automation-portfolio/actions/workflows/pytest.yml/badge.svg)](https://github.com/AlanCano2710/qa-automation-portfolio/actions/workflows/pytest.yml)

## Project overview

This repository is a **browser-based UI test automation** portfolio. It demonstrates how to build a maintainable Selenium suite with **pytest**, using real public applications—primarily **[SauceDemo](https://www.saucedemo.com)** for login, cart, checkout, and logout flows—and configurable targets for lighter smoke checks.

The project is intended for reviewers and hiring managers: it shows **clear structure** (configuration, page objects, utilities, tests), **repeatable local runs**, **HTML execution reports**, **failure evidence** (screenshots), **flaky-test mitigation** via automatic reruns, and **continuous integration** on GitHub so the same tests execute on every change without manual setup.

---

## Architecture: Page Object Model (POM)

Automation is organized around the **Page Object Model**. Each screen (or coherent UI area) is represented by a **page class** under `pages/` that owns **locators** and **user-level actions** (for example, “log in”, “add item to cart”). **Tests** under `tests/` stay focused on **behavior and assertions**; they call page methods instead of scattering raw Selenium calls across files.

Shared concerns are centralized:

| Layer | Responsibility |
|--------|------------------|
| **`pages/`** | Page objects inheriting `BasePage`; explicit waits for stable interaction |
| **`src/`** | Environment-driven settings (`config.py`) |
| **`utils/`** | WebDriver creation, wait helpers, failure screenshot helpers |
| **`tests/`** | Test cases, pytest fixtures (`conftest.py`), hooks for reports and screenshots |

This separation keeps UI changes localized to page objects and makes failures easier to diagnose.

---

## Tech stack

| Area | Choice |
|------|--------|
| Language | Python 3.10+ (CI uses 3.11) |
| Test runner | [pytest](https://pytest.org/) |
| Browser automation | [Selenium 4](https://www.selenium.dev/) WebDriver |
| Drivers | [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) (Chrome, Firefox, Edge) |
| HTML reports | [pytest-html](https://pytest-html.readthedocs.io/) (self-contained HTML) |
| Flaky tests | [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures) (failed tests rerun up to **2** extra times; see `pytest.ini`) |
| CI | [GitHub Actions](https://docs.github.com/en/actions) on Ubuntu with Chrome |

---

## Test types (markers)

Markers are registered in **`pytest.ini`** under `markers`. They document intent and let you run subsets of the suite.

| Marker | Intent | Typical use |
|--------|--------|------------|
| **`smoke`** | Fast checks that critical paths work | Pre-merge or CI sanity |
| **`regression`** | Broader coverage beyond smoke | Nightly or before release |
| **`e2e`** | End-to-end flows through multiple UI steps | Full user journeys |

**Examples**

```bash
pytest -m smoke
pytest -m regression
pytest -m "smoke or regression"
```

---

## CI integration

The suite is wired to **GitHub Actions**: every **push** and every **pull request** triggers a workflow that installs Python, installs Chrome, runs **pytest** in **headless** mode, and uploads generated artifacts under `reports/` for inspection when something fails.

Status at a glance: use the **CI badge** at the top of this README, or open the **Actions** tab on the repository.

---

## How to run locally

### Prerequisites

- Python **3.10+** recommended  
- A supported browser: **Chrome**, **Firefox**, or **Microsoft Edge** (for local non-headless runs)

### Virtual environment

**Windows (PowerShell)**

```powershell
cd path\to\qa-automation-portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
cd path/to/qa-automation-portfolio
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run tests

Always run from the **project root** so `pytest.ini` (including `pythonpath` and default options) applies.

```bash
pytest
```

Common commands:

| Goal | Command |
|------|---------|
| Verbose output | `pytest -v` |
| Smoke tests only | `pytest -m smoke` |
| List tests without running | `pytest --collect-only` |
| Headless (similar to CI) | PowerShell: `$env:HEADLESS="true"; pytest` — bash: `HEADLESS=true pytest` |

Optional environment variables are documented in **`src/config.py`** (for example `BASE_URL`, `BROWSER`, `HEADLESS`, `IMPLICIT_WAIT`, `PAGE_LOAD_TIMEOUT`, `EXPLICIT_WAIT`, `WINDOW_WIDTH`, `WINDOW_HEIGHT`).

### HTML report path (override)

```bash
pytest --html=reports/smoke_report.html --self-contained-html -m smoke
```

### Flaky test retries

By default, **`pytest.ini`** includes **`--reruns 2`**: a failing test may run up to **two** additional times (up to **three** attempts total). To disable retries while debugging:

```bash
pytest --reruns 0
```

---

## How CI works

The workflow lives at **`.github/workflows/pytest.yml`**.

| Aspect | Detail |
|--------|--------|
| **Name** | Python Pytest CI |
| **Triggers** | Push to any branch; pull requests |
| **Runner** | `ubuntu-latest` |
| **Runtime** | Python **3.11**; pip dependencies cached |
| **Browser** | Chrome installed via **browser-actions/setup-chrome** |
| **Execution** | `pytest -v` with **`HEADLESS=true`** |
| **CI behavior** | GitHub sets **`CI=true`**, which **increases Selenium timeouts** in `src/config.py` for shared runners |

After the run, the workflow uploads the **`reports/`** directory as an artifact named **`pytest-reports`** (upload runs even when tests fail, so HTML reports and failure screenshots remain available).

**Where to look:** GitHub → **Actions** → select the workflow run → download **pytest-reports** if you need the HTML report or PNGs.

---

## Example report

Each run produces a **single self-contained HTML file** (no extra assets).

- **Default file:** `reports/report.html`  
- **Contents:** Pass/fail/skip summary, duration, environment metadata, and failure details suitable for sharing or archiving.

Open locally:

- **Windows:** `start reports\report.html` (PowerShell) or open the file in a browser  
- **macOS:** `open reports/report.html`  
- **Linux:** `xdg-open reports/report.html`

**Failure screenshots:** When a test uses the `driver` fixture and fails, a PNG is saved under **`reports/screenshots/`**. Naming pattern: **`{module}__{test_name}__{YYYYMMDD_HHMMSS}.png`**. On **Chrome and Edge**, full-page capture is used when available (DevTools); other browsers may use a viewport screenshot. See **`utils/screenshot_helpers.py`** and **`tests/conftest.py`**.

---

## Project structure

```
qa-automation-portfolio/
├── .github/
│   └── workflows/
│       └── pytest.yml          # GitHub Actions: install, pytest, upload reports
├── src/
│   └── config.py               # Settings from environment (URLs, browser, timeouts)
├── pages/
│   ├── base_page.py            # Shared waits and navigation helpers
│   └── saucedemo_login_page.py # SauceDemo page object(s)
├── utils/
│   ├── driver_factory.py       # WebDriver setup (Chrome / Firefox / Edge)
│   ├── wait_helpers.py         # Extra explicit wait utilities
│   └── screenshot_helpers.py   # Failure PNGs (full page on Chromium when possible)
├── tests/
│   ├── conftest.py             # Fixtures, failure screenshots, pytest hooks
│   ├── test_*.py               # Test modules
├── pytest.ini                  # Markers, reruns, HTML report defaults
├── requirements.txt
└── reports/                    # Generated: HTML report, screenshots (local/CI artifact)
```

| Path | Role |
|------|------|
| **`src/`** | Central configuration; no UI locators |
| **`pages/`** | Page Object Model: one place per screen for selectors and actions |
| **`utils/`** | Cross-cutting helpers (drivers, waits, screenshots) |
| **`tests/`** | Specifications and pytest infrastructure |
| **`pytest.ini`** | Discovery, markers, CLI defaults (`--reruns`, `--html`, etc.) |
| **`reports/`** | Output only; safe to delete between runs |

---

## Configuration reference

| Variable | Purpose | Typical default |
|----------|---------|-----------------|
| `BASE_URL` | Application under test | `https://example.com` |
| `BROWSER` | `chrome`, `firefox`, or `edge` | `chrome` |
| `IMPLICIT_WAIT` | Implicit wait (seconds) | Higher when `CI=true` |
| `PAGE_LOAD_TIMEOUT` | Page load timeout (seconds) | Higher when `CI=true` |
| `EXPLICIT_WAIT` | Default explicit wait in page objects | Higher when `CI=true` |
| `HEADLESS` | Run without UI | `false` locally; `true` in CI |
| `WINDOW_WIDTH` / `WINDOW_HEIGHT` | Browser window size | `1280` × `720` |

---

## Extending the suite

1. Add or extend page classes under **`pages/`** (inherit **`BasePage`**).  
2. Add tests under **`tests/`** using the **`driver`** and **`settings`** fixtures.  
3. Apply **`@pytest.mark.smoke`**, **`regression`**, or **`e2e`** as appropriate.  
4. Point **`BASE_URL`** at your environment and adjust locators.

---

## Troubleshooting

- **Import errors:** Run pytest from the repository root.  
- **Driver issues:** Install a matching browser; `webdriver-manager` resolves drivers for local runs.  
- **Timeouts on CI:** `CI=true` already relaxes timeouts; override env vars if your app is slow.  
- **Missing HTML report:** Run `pip install -r requirements.txt` and ensure `pytest.ini` is picked up (run from project root).

---

## License

Use this portfolio project as you see fit for learning and interviews.
