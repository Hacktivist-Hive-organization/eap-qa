from playwright.sync_api import Page


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("#register-first-name")
        self.last_name = page.locator("#register-last-name")
        self.register_email = page.locator("#register-email")
        self.register_password = page.locator("#register-password")
        self.signup_button = page.get_by_role('button', name='Sign Up')

    def go_to_register_page(self):
        self.page.goto("/register")

    def set_first_name(self, value):
        self.first_name.fill(value)

    def set_last_name(self, value):
        self.last_name.fill(value)

    def set_register_email(self, value):
        self.register_email.fill(value)

    def set_register_password(self, value):
        self.register_password.fill(value)

    def click_signup_button(self):
        self.signup_button.click()

    def register_new_user(self, first_name: str, last_name: str, email: str, password: str):
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_register_email(email)
        self.set_register_password(password)
        self.click_signup_button()
