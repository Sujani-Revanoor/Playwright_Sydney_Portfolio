import os
import allure
import pytest
from playwright.sync_api import Page


# session-scoped fixture runs once per test run (across all workers/tests)
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Customize the default Playwright browser context created by pytest-playwright.
    A 'context' is like an isolated incognito browser session (cookies, storage, viewport).
    """
    return {
        # Keep any existing arguments passed via CLI or pytest-playwright defaults
        **browser_context_args,
        # Set a consistent desktop viewport so elements don't shift or hide responsively
        "viewport": {"width": 1920, "height": 1080},
        # Helpful for test/staging environments that use self-signed SSL certificates
        "ignore_https_errors": True,
    }


# autouse=True means every UI test that uses 'page' automatically runs this fixture
@pytest.fixture(autouse=True)
def capture_failure_artifacts(request, page: Page):
    """
    Records a Playwright Trace before each test runs.
    If the test fails, attaches a full-page screenshot and trace .zip to Allure;
    otherwise discards the trace to save disk space.
    """
    # Access the browser context that owns this 'page' (browser tab)
    context = page.context

    # Start recording actions, DOM snapshots, screenshots, and network/console activity
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # 'yield' hands control back to the test function while it executes
    yield

    # Everything after 'yield' runs as teardown once the test finishes
    os.makedirs("reports/traces", exist_ok=True)

    # Check if the main test body ('rep_call', attached by the hook below) failed
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        # 1. Capture a full-page PNG screenshot at the exact moment of failure
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"failure_screenshot_{request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )

        # 2. Stop tracing and save the .zip file so you can open it in Playwright Trace Viewer
        trace_path = f"reports/traces/{request.node.name}.zip"
        context.tracing.stop(path=trace_path)

        # 3. Attach the trace archive to the Allure report for debugging
        allure.attach.file(
            trace_path,
            name=f"playwright_trace_{request.node.name}",
            extension="zip",
        )
    else:
        # Stop tracing without saving a file when the test passes
        context.tracing.stop()


# Hook that stores each test phase result (setup, call, teardown) onto the test item 'request.node'
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)