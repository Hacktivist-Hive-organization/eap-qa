from playwright.sync_api import expect
from e2e_tests.ui.pages.search_page import SearchPage
import pytest


@pytest.mark.ui
def test_go_to_example_page(page):
    page.goto("/")  # uses base_url from context
    start_page = SearchPage(page)
    expect(start_page.get_started_link).to_have_text("Get started")