import pytest
from playwright.sync_api import sync_playwright, Page
import utils

CONFIG_PATH = "config.ini"


@pytest.fixture(scope="session")
def config():
    return utils.load_config(path=CONFIG_PATH)


@pytest.fixture(scope="function")
def browser(config):
    ui_config = config["ui"]
    browser_name = ui_config.get("browser_name")
    with sync_playwright() as p:
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=ui_config.get("headless"))
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=ui_config.get("headless"))
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=ui_config.get("headless"))

        yield browser
        browser.close()


@pytest.fixture(scope="function")
def browser_context(config, browser):
    ui_config = config["ui"]
    base_url = ui_config.get("base_url")
    ctx = browser.new_context(base_url=base_url)
    yield ctx
    ctx.close()
