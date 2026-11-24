# Playwright Python End-to-End & API Automation Framework

A scalable test automation framework built with **Playwright**, **Python**, **Pytest**, **Allure Reporting**, and **GitLab CI/CD**. Designed around modern QA Engineering best practices—including Page Object Model (POM), parallel execution, automatic failure tracing, and live report publishing via GitLab Pages.

> **Live Allure Test Report:** `https://<your-gitlab-username>.gitlab.io/<your-repo-name>/`

---

## Key Engineering Highlights

* **Hybrid UI & API Automation:** Combines browser-based E2E tests (`Page`) with fast REST API contract validation (`APIRequestContext`) in a unified Python framework.
* **Resilient Locators & Auto-Waiting:** Uses user-facing Playwright locators (`get_by_role`, `get_by_placeholder`) and web-first `expect()` assertions to eliminate flaky waits.
* **Parallel Execution:** Configured with `pytest-xdist` (`-n auto`) to distribute tests across CPU workers for fast feedback.
* **Automated Failure Diagnostics:** Pytest fixtures in `tests/conftest.py` capture full-page screenshots and interactive **Playwright Trace `.zip`** archives only on test failure and attach them directly to Allure.
* **Containerized GitLab CI/CD Pipeline:** Runs inside Microsoft's official Playwright Docker image and automatically deploys interactive Allure HTML dashboards to **GitLab Pages** on `main`.

---

## Project Architecture

```text
Playwright_Sydney_Portfolio/
├── .gitlab-ci.yml              # GitLab CI/CD pipeline (Test -> Allure -> GitLab Pages)
├── pytest.ini                  # Pytest parallel flags, markers & Allure output config
├── requirements.txt            # Python dependencies
├── .gitignore                  # Excludes .venv, reports, traces, and IDE files
├── pages/
│   └── login_page.py           # Page Object Model encapsulating locators & actions
├── tests/
│   ├── conftest.py             # Browser context setup, failure screenshots & trace hooks
│   ├── ui/
│   │   └── test_login.py       # Smoke & parameterized regression UI tests
│   └── api/
│       └── test_users_api.py   # REST API status & JSON schema validation
└── reports/                    # Git-ignored local Allure results & Playwright traces