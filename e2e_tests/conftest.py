from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, expect
from e2e_tests.utils import settings
import uuid
import os
from e2e_tests.api.api_client import ApiClient
from test_data.fixtures.auth_fixtures import make_user, registered_user, access_token, auth_headers
from test_data.fixtures.request_fixtures import make_request, create_request, request_payloads, request_types_map, \
    request_types

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.ini"
TRACES_DIR_PATH = Path.cwd().joinpath("artifacts").joinpath("traces")


@pytest.fixture(scope="session")
def config():
    cfg = settings.load_config(path=CONFIG_PATH)
    return cfg


@pytest.fixture(scope="session")
def browser(config):
    expect.set_options(timeout=15000)
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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # injecting the result to test object
    outcome = yield
    rep = outcome.get_result()
    # rep_setup, rep_call, rep_teardown
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function", autouse=True)
def trace_browser_context(request, config, browser_context):
    ui_config = config["ui"]
    save_trace = ui_config.get("save_trace")
    # if save_trace config is on or retain-on-failure
    if save_trace == "off":
        yield
        return

    if save_trace != "off":
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if save_trace == "on" or (save_trace == "retain-on-failure" and failed):
        test_name = request.node.name
        browser_context.tracing.stop(path=TRACES_DIR_PATH.joinpath(f"trace-{test_name}-{uuid.uuid4()}.zip"))


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
