# QA Automation Portfolio

[![Python Pytest CI](https://github.com/AlanCano2710/qa-automation-portfolio/actions/workflows/pytest.yml/badge.svg)](https://github.com/AlanCano2710/qa-automation-portfolio/actions/workflows/pytest.yml)

## Project description

This repository is a **portfolio-grade UI test automation** project. It demonstrates end-to-end browser testing with **Selenium**, organized using the **Page Object Model (POM)** so locators and user actions stay separate from test assertions. Tests target public demo sites (for example [SauceDemo](https://www.saucedemo.com)) and configurable base URLs for smoke and regression scenarios.

The suite includes **pytest** fixtures for browser lifecycle, **HTML reports** after each run, **failure screenshots**, and a **GitHub Actions** workflow so the same tests run automatically on every push.

## Tech stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.10+ (CI uses 3.11) |
| Test runner | [pytest](https://pytest.org/) |
| Browser automation | [Selenium 4](https://www.selenium.dev/) WebDriver |
| Drivers | [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) (Chrome, Firefox, Edge) |
| Reporting | [pytest-html](https://pytest-html.readthedocs.io/) (self-contained HTML) |
| CI | [GitHub Actions](https://docs.github.com/en/actions) (Ubuntu, Chrome, headless) |

Project layout: **`src/`** (configuration), **`pages/`** (page objects), **`utils/`** (driver factory and helpers), **`tests/`** (specs and `conftest.py`).

## How to run tests

### 1. Environment

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

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Execute tests

Run the full suite from the **project root** (so `pytest.ini` applies):

```bash
pytest
```

Useful variants:

| Goal | Command |
|------|---------|
| Verbose output | `pytest -v` |
| Smoke tests only | `pytest -m smoke` |
| List tests without running | `pytest --collect-only` |
| Headless browser (CI-like) | `$env:HEADLESS="true"` then `pytest` (PowerShell) or `HEADLESS=true pytest` (bash) |

Optional environment variables (see `src/config.py`): `BASE_URL`, `BROWSER`, `HEADLESS`, `IMPLICIT_WAIT`, `PAGE_LOAD_TIMEOUT`, `WINDOW_WIDTH`, `WINDOW_HEIGHT`.

Custom HTML report path:

```bash
pytest --html=reports/smoke_report.html --self-contained-html -m smoke
```

## Example report

After any successful `pytest` run, **pytest-html** writes a **single self-contained HTML file** you can open in a browser—no extra assets required.

- **Default path:** `reports/report.html`
- **Contents:** test outcomes (pass/fail/skip), duration, environment metadata, and failure details from pytest.

Open the report locally:

- **Windows:** double-click `reports\report.html` or run `start reports\report.html` in PowerShell.
- **macOS:** `open reports/report.html`
- **Linux:** `xdg-open reports/report.html`

Failure screenshots (when a test using the `driver` fixture fails) are saved under `reports/screenshots/` and referenced implicitly by the failing test context in the console; the HTML report lists the run summary.

## CI workflow explanation

A GitHub Actions workflow runs the same pytest suite in the cloud **without manual steps**.

| Item | Detail |
|------|--------|
| **File** | `.github/workflows/pytest.yml` |
| **Name** | Python Pytest CI |
| **Triggers** | Every **push** to any branch and every **pull_request** |
| **Runner** | `ubuntu-latest` |
| **Steps (summary)** | Checkout code → install Python 3.11 (with pip cache) → install Chrome → `pip install -r requirements.txt` → run `pytest -v` with `HEADLESS=true` → upload `reports/` as artifact `pytest-reports` (runs even if tests fail, so HTML report and screenshots are available for debugging) |

To view results: open the **Actions** tab on GitHub, select the workflow run, then download the **pytest-reports** artifact if you need the generated HTML and screenshot files.

## Project layout

| Path | Purpose |
|------|---------|
| `src/` | Shared configuration (`config.py`) |
| `pages/` | Page Object classes |
| `utils/` | WebDriver factory, wait helpers |
| `tests/` | Tests and `conftest.py` (fixtures, failure screenshots) |
| `pytest.ini` | Pytest defaults, markers, HTML report flags |
| `requirements.txt` | Dependencies |
| `reports/` | Generated HTML report and failure screenshots (gitignored or local only) |
| `.github/workflows/` | CI definitions |

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Application under test | `https://example.com` |
| `BROWSER` | `chrome`, `firefox`, or `edge` | `chrome` |
| `IMPLICIT_WAIT` | Implicit wait (seconds) | `10` |
| `PAGE_LOAD_TIMEOUT` | Page load timeout (seconds) | `30` |
| `HEADLESS` | `true` / `false` | `false` |
| `WINDOW_WIDTH` | Browser width (pixels) | `1280` |
| `WINDOW_HEIGHT` | Browser height (pixels) | `720` |

## Practices used

1. **Page Object Model** — Locators and actions live in `pages/`; tests assert behavior.
2. **Fixtures** — `driver` and `settings` in `tests/conftest.py`.
3. **Explicit waits** — Prefer `WebDriverWait` in `BasePage` / `utils/wait_helpers.py`.
4. **Markers** — `smoke`, `regression`, `e2e` in `pytest.ini`.
5. **No secrets in repo** — Use CI secrets or local `.env` (gitignored).

## Extending the suite

1. Add page classes under `pages/` (inherit `BasePage`).
2. Add tests under `tests/` using the `driver` and `settings` fixtures.
3. Set `BASE_URL` and adjust locators for your application.

## Troubleshooting

- **Driver / browser mismatch** — Ensure the browser is installed; `webdriver-manager` resolves drivers locally.
- **Import errors** — Run pytest from the project root.
- **Flaky tests** — Increase explicit wait timeouts on slow networks or CI.
- **HTML report missing** — Run `pip install -r requirements.txt` and execute pytest from the project root.

## License

Use this portfolio project as you see fit for learning.
