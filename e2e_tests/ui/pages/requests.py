from playwright.sync_api import Page


class RequestsPage:
    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_text('all Requests Dashboard')
        self.logout_button = page.get_by_role('button', name='Logout')

    def click_logout_button(self):
        self.logout_button.click()