import allure
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


# @allure.feature groups these tests under "UI Authentication" in the Allure report
@allure.feature("UI Authentication")
class TestLogin:
    """
    End-to-end UI login tests using the LoginPage Page Object.
    """

    # @pytest.mark.smoke tags this as a critical path test (run via: pytest -m smoke)
    @pytest.mark.smoke
    @allure.title("Verify valid user can log in and view Products page")
    def test_valid_login(self, page: Page):
        # 'page' is provided automatically by the pytest-playwright plugin
        # (and already has your session viewport + tracing fixture applied)
        login_page = LoginPage(page)

        # Execute the login flow defined in LoginPage
        login_page.login("standard_user", "secret_sauce")

        # expect() is Playwright's web-first assertion: it automatically retries
        # until the condition passes or times out (default 5 seconds), which
        # avoids race conditions and flaky assertions on dynamic UIs.
        expect(page.locator(".title")).to_have_text("Products")

    # @pytest.mark.regression tags broader scenarios; @pytest.mark.parametrize
    # runs this single test function once per tuple in the list below
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            # Case 1: Locked out user account
            ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
            # Case 2: Valid user with wrong password
            ("standard_user", "wrong_password", "Username and password do not match"),
        ],
    )
    @allure.title("Verify error message for invalid login: {username}")
    def test_invalid_login(self, page: Page, username: str, password: str, expected_error: str):
        login_page = LoginPage(page)
        login_page.login(username, password)

        # Verify the error banner appears on screen
        expect(login_page.error_banner).to_be_visible()

        # Verify the error message contains the expected text
        expect(login_page.error_banner).to_contain_text(expected_error)