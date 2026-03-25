# QA Automation Portfolio

Professional **Python** test automation using **pytest** and **Selenium** with a maintainable **Page Object Model (POM)** layout.

## Features

- **pytest** for discovery, fixtures, markers, and reporting
- **Selenium 4** WebDriver with **webdriver-manager** (drivers aligned to your installed browser)
- Clear separation: **`src/`** (config), **`pages/`** (UI abstraction), **`utils/`** (drivers and helpers), **`tests/`** (specs)
- Environment-based configuration (no secrets in code)

## Requirements

- Python **3.10+** recommended
- A supported browser: **Chrome**, **Firefox**, or **Microsoft Edge** (installed on the machine running tests)

## Quick start

### 1. Create and activate a virtual environment

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

### 3. Run tests

```bash
pytest
```

Run only smoke tests:

```bash
pytest -m smoke
```

List tests without executing:

```bash
pytest --collect-only
```

## Project layout

| Path | Purpose |
|------|---------|
| `src/` | Shared configuration (`config.py`) and package docs |
| `pages/` | Page Object classes: locators and user-level actions per screen |
| `utils/` | WebDriver factory, explicit wait helpers |
| `tests/` | Test modules and `conftest.py` (fixtures) |
| `pytest.ini` | Pytest defaults, markers, `pythonpath` |
| `requirements.txt` | Pinned dependency stack |

## Configuration

Settings are loaded in `src/config.py` via `load_settings()`. You can override defaults with environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Application under test | `https://example.com` |
| `BROWSER` | `chrome`, `firefox`, or `edge` | `chrome` |
| `IMPLICIT_WAIT` | Implicit wait (seconds) | `10` |
| `PAGE_LOAD_TIMEOUT` | Page load timeout (seconds) | `30` |
| `HEADLESS` | `true` / `false` | `false` |
| `WINDOW_WIDTH` | Browser width (pixels) | `1280` |
| `WINDOW_HEIGHT` | Browser height (pixels) | `720` |

**Example (PowerShell)**

```powershell
$env:BASE_URL = "https://example.com"
$env:HEADLESS = "true"
pytest -m smoke
```

## Practices used

1. **Page Object Model** — Tests call page methods; locators live in page classes.
2. **Fixtures** — `driver` and `settings` in `tests/conftest.py` keep tests short and consistent.
3. **Explicit waits** — Prefer `WebDriverWait` (see `BasePage` and `utils/wait_helpers.py`) over fixed `sleep()` except when unavoidable.
4. **Markers** — `@pytest.mark.smoke`, `regression`, `e2e` registered in `pytest.ini` for selective runs.
5. **No secrets in repo** — Use `.env` locally (gitignored) or CI variables; never commit credentials.

## Extending the suite

1. Add a new page class under `pages/` (inherit `BasePage`).
2. Add tests under `tests/` that use the `driver` and `settings` fixtures.
3. Point `BASE_URL` at your environment and adjust locators to match your app.

## Troubleshooting

- **Driver / browser mismatch** — `webdriver-manager` downloads a matching driver; ensure the browser is installed and up to date.
- **Import errors** — Run pytest from the project root so `pytest.ini` `pythonpath = .` applies.
- **Flaky tests** — Increase explicit wait timeouts on slow environments; avoid sharing one browser across parallel tests without isolation strategy.

## License

Use this portfolio project as you see fit for learning and interviews.
