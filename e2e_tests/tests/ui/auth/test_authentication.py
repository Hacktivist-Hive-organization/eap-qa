from playwright.sync_api import Page, expect
from e2e_tests.ui.pages.login import LoginPage
from e2e_tests.ui.pages.requests import RequestsPage
from e2e_tests.ui.pages.register import RegisterPage
import pytest

from test_data.fixtures.auth_fixtures import make_user


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    return RegisterPage(page)


@pytest.fixture
def requests_page(page: Page) -> RequestsPage:
    return RequestsPage(page)


@pytest.mark.ui
def test_register_with_new_user(register_page, requests_page, make_user):
    user = make_user()
    register_page.go_to_register_page()
    register_page.register_new_user(user["first_name"], user["last_name"], user["email"], user["password"])
    expect(requests_page.page_title).to_be_visible()


@pytest.mark.ui
def test_login_with_valid_credentials(login_page, requests_page, registered_user):
    user = registered_user
    login_page.go_to_login_page()
    login_page.login_to_application(user["email"], user["password"])
    # verify that user navigates to requests dashboard
    expect(requests_page.page_title).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize("email,password", [("non@existing.email", "Psw!1234")])
def test_login_with_non_existing_email(login_page, email, password):
    login_page.go_to_login_page()
    login_page.login_to_application(email, password)
    # verify warning
    expect(login_page.login_error_toast).to_be_visible()


@pytest.mark.ui
def test_login_with_wrong_password(login_page, registered_user):
    user = registered_user
    login_page.go_to_login_page()
    login_page.login_to_application(user["email"], "Wrong_pas1")
    expect(login_page.login_error_toast).to_be_visible()


@pytest.mark.ui
def test_user_logout(login_page, requests_page, registered_user):
    user = registered_user
    login_page.go_to_login_page()
    login_page.login_to_application(user["email"], user["password"])
    expect(requests_page.page_title).to_be_visible()
    requests_page.click_logout_button()
    expect(login_page.sign_in_button).to_be_visible()
