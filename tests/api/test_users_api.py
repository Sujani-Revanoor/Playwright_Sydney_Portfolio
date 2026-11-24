import allure
import pytest
from playwright.sync_api import Playwright


# @allure.feature groups API checks under a dedicated feature in the Allure report
@allure.feature("Users REST API")
# @pytest.mark.api lets you run only API tests via: pytest -m api
@pytest.mark.api
@allure.title("Verify GET /api/users returns 200 OK and expected user payload")
def test_get_users_list(playwright: Playwright):
    """
    Demonstrates Playwright's built-in APIRequestContext for backend/API validation.
    Using one framework for both UI and API checks is a strong talking point for
    Sydney SDET and QA Automation interviews.
    """
    # Create an isolated API request context with a base URL (no browser launches)
    api_context = playwright.request.new_context(base_url="https://reqres.in")

    # Send an HTTP GET request to the endpoint with query parameter page=2
    response = api_context.get("/api/users?page=2")

    # Check the HTTP status code (200 means OK)
    assert response.status == 200, f"Expected status 200, but got {response.status}"

    # Parse the JSON response body into a Python dict so we can inspect fields
    payload = response.json()

    # Verify top-level response structure and non-empty list
    assert "data" in payload, "Expected 'data' key in API response JSON"
    assert len(payload["data"]) > 0, "Expected at least one user record in 'data'"

    # Verify the first user object contains an 'email' field
    first_user = payload["data"][0]
    assert "email" in first_user, "Expected 'email' field on user object"

    # Dispose of the API context to release network/session resources cleanly
    api_context.dispose()