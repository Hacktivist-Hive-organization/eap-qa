from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from e2e_tests.utils import settings
import uuid
import os
from e2e_tests.api.api_client import ApiClient
from test_data.fixtures.auth_fixtures import make_user

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.ini"
TRACES_DIR_PATH = Path.cwd().joinpath("artifacts").joinpath("traces")


@pytest.fixture(scope="session")
def config():
    cfg = settings.load_config(path=CONFIG_PATH)
    return cfg


@pytest.fixture(scope="function")
def browser(config):
    ui_config = config["ui"]
    browser_name = ui_config.get("browser_name")
    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=ui_config.getboolean("headless"))
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=ui_config.getboolean("headless"))
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=ui_config.getboolean("headless"))
        else:
            raise RuntimeError(f"Unknown browser: {browser_name}")

        yield browser
        browser.close()


@pytest.fixture(scope="function")
def browser_context(config, browser):
    ui_config = config["ui"]
    base_url = ui_config.get("base_url")
    ctx = browser.new_context(base_url=base_url)

    yield ctx
    ctx.close()


@pytest.fixture(scope="function", autouse=True)
def trace_browser_context(config, browser_context):
    ui_config = config["ui"]
    save_trace = ui_config.getboolean("save_trace")

    if save_trace:
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    if save_trace:
        browser_context.tracing.stop(path=TRACES_DIR_PATH.joinpath(f"trace-{uuid.uuid4()}.zip"))


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page

    page.close()


@pytest.fixture(scope="session")
def api_url(config):
    api_config = config["api"]
    return os.getenv("API_BASE_URL", api_config.get("api_url"))


@pytest.fixture(scope="session")
def api_client(api_url):
    client = ApiClient(api_url)
    yield client
    client.close()
