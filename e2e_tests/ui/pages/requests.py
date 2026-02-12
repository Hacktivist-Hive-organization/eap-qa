from playwright.sync_api import Page, expect


class RequestsPage:
    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_text('all Requests Dashboard')
        self.account_button = page.locator('[data-slot="dropdown-menu-trigger"]')
        self.logout_button = page.get_by_role("menuitem", name='Logout')

    def click_logout_button(self):
        self.account_button.click()
        expect(self.logout_button).to_be_visible()
        self.logout_button.click()