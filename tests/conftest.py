import os
import allure
import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture
def api_client(playwright: Playwright) -> APIRequestContext:
    base_url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    token = os.getenv("API_TOKEN")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers=headers,
        timeout=10_000,
    )
    yield context
    context.dispose()


@pytest.fixture(autouse=True)
def capture_failure_artifacts(request):
    if "page" not in request.fixturenames:
        yield
        return

    page: Page = request.getfixturevalue("page")
    context = page.context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    os.makedirs("reports/traces", exist_ok=True)
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"failure_screenshot_{request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )

        trace_path = f"reports/traces/{request.node.name}.zip"
        context.tracing.stop(path=trace_path)

        allure.attach.file(
            trace_path,
            name=f"playwright_trace_{request.node.name}",
            extension="zip",
        )
    else:
        context.tracing.stop()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)