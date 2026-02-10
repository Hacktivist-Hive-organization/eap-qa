from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.page_title = "Login"
        self.email_button = page.locator("#login-email")
        self.password_button = page.locator("#login-password")
        self.sign_in_button = page.get_by_role('button', name='Sign In')
        self.login_error_toast = page.locator("[data-sonner-toast][data-type='error'][data-visible='true']")

    def go_to_login_page(self):
        self.page.goto("/login")

    def set_email(self, value):
        self.email_button.fill(value)

    def set_password(self, value):
        self.password_button.fill(value)

    def click_submit_button(self):
        self.sign_in_button.click()

    def login_to_application(self, email: str, password: str):
        self.set_email(email)
        self.set_password(password)
        self.click_submit_button()
