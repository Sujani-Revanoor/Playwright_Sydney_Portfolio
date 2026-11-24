import allure
from playwright.sync_api import Page


class LoginPage:
    """
    Page Object Model (POM) class representing the Login page.
    Keeping locators and actions here prevents duplicating selectors across test files
    and makes maintenance much easier if the UI changes.
    """

    def __init__(self, page: Page):
        # 'page' represents a single browser tab/page in Playwright
        self.page = page

        # --- Locators ---
        # Playwright recommends user-facing locators (role, label, placeholder, test ID)
        # over brittle XPath/CSS selectors because they mirror how real users interact.

        # Matches an <input> element with placeholder="Username"
        self.username_input = page.get_by_placeholder("Username")

        # Matches an <input> element with placeholder="Password"
        self.password_input = page.get_by_placeholder("Password")

        # Matches a button with accessible name/text "Login"
        self.login_button = page.get_by_role("button", name="Login")

        # Matches an element with attribute data-test="error" (common on SauceDemo)
        self.error_banner = page.locator("[data-test='error']")

    # @allure.step turns this method into a clearly labeled step in the Allure report
    @allure.step("Open login page and sign in as '{username}'")
    def login(self, username: str, password: str):
        # Navigate to the application URL; 'domcontentloaded' waits until HTML is parsed
        self.page.goto("https://www.saucedemo.com", wait_until="domcontentloaded")

        # .fill() automatically waits for the input to be visible and enabled,
        # clears any existing value, and types the text immediately (faster than .type())
        self.username_input.fill(username)
        self.password_input.fill(password)

        # .click() automatically checks actionability (visible, stable, not obscured)
        # before clicking the button—no manual WebDriverWait or sleep needed
        self.login_button.click()