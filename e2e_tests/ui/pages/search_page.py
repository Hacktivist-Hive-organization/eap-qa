from playwright.sync_api import Page


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.get_started_link = page.get_by_role("link", name="Get started")