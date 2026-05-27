# Django Poll App QA Project

This repository contains my Software Quality Assurance final project for MPCS 56540. The project is based on the open-source Django Poll App and includes QA artifacts such as linting, user acceptance testing, unit tests, coverage reports, performance testing, UI automation, integration tests, code smell review, and CI/CD configuration.

## Reference Codebase

Original repository: https://github.com/devmahmud/Django-Poll-App

This repository contains my modified version of the app with added tests, reports, configurations, and project documentation.

---

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/sandyzhengg23/Django-Poll-App.git
cd Django-Poll-App
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install project dependencies:

```bash
python -m pip install -r requirements.txt
```

Install QA/testing dependencies:

```bash
python -m pip install ruff pytest pytest-django pytest-cov
```

Run database migrations:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

Open the app in the browser:

```text
http://127.0.0.1:8000/
```

---

## Running the Linter

This project uses Ruff for static analysis. Ruff is configured in `pyproject.toml`.

Run the linter:

```bash
ruff check .
```

Optional: save linter output to a report file:

```bash
mkdir -p reports/linter
ruff check . > reports/linter/ruff_initial.txt || true
```

---

## Q2: User Acceptance Testing

The UAT test suite is included at:

```text
reports/uat/UAT_Test_suite.xlsx
```

The UAT suite includes manual test cases with:

* Test Case ID
* Test Case Name
* Description
* Preconditions
* Steps
* Expected Result
* Actual Result
* Pass/Fail
* Black-box Technique Used

Screenshots of the authored and executed UAT suite are included in the project write-up.

---

## Q3: Unit Tests

The unit tests are located in:

```text
tests/unit/
```

Unit test files:

```text
tests/unit/test_forms_unit.py
tests/unit/test_views_unit.py
```

The suite contains 8 unit tests total. Four tests cover form validation, and four tests use test doubles to isolate view behavior from shared dependencies such as the database, authenticated user objects, Django messages, redirects, and vote persistence.

The test double types used include:

* Dummy
* Stub
* Mock
* Spy

### Run Unit Tests

A grader can run the full unit test suite with:

```bash
python -m pytest tests/unit
```

### Run Unit Tests with Coverage

A grader can run the unit tests with coverage using:

```bash
mkdir -p reports/coverage

python -m pytest tests/unit \
  --cov=accounts \
  --cov=polls \
  --cov-report=term-missing \
  --cov-report=html:reports/coverage/htmlcov
```

### Save Coverage Output to a Text Report

```bash
python -m pytest tests/unit \
  --cov=accounts \
  --cov=polls \
  --cov-report=term-missing \
  --cov-report=html:reports/coverage/htmlcov \
  > reports/coverage/unit_test_coverage.txt
```

### Open HTML Coverage Report

On macOS:

```bash
open reports/coverage/htmlcov/index.html
```

The coverage report is stored in:

```text
reports/coverage/
```

## Q4: Performance Testing

This project uses **k6** for performance testing. The performance tests are located in:

```text
performance/load_test.js
performance/spike_test.js


The two performance test types are:

* Load test: tests the app under normal expected traffic
* Spike test: tests the app under a sudden traffic increase

The tested endpoints are:

```text
/
 /accounts/login/
 /accounts/register/
```

### Install k6

On macOS, install k6 with Homebrew:

```bash
brew install k6
```

Check that k6 is installed:

```bash
k6 version
```

### Run the Django Server

Before running the performance tests, start the Django app in one terminal:

```bash
python manage.py runserver
```

The app should be running at:

```text
http://127.0.0.1:8000/
```

### Run the Load Test

In a second terminal, run:

```bash
k6 run performance/load_test.js
```

To save the load test output to a report file:

```bash
mkdir -p reports/performance
k6 run performance/load_test.js > reports/performance/load_test_summary.txt
```

### Run the Spike Test

```bash
k6 run performance/spike_test.js
```

To save the spike test output to a report file:

```bash
mkdir -p reports/performance
k6 run performance/spike_test.js > reports/performance/spike_test_summary.txt
```

The raw performance test summaries are stored in:

```text
reports/performance/
```

Screenshots of the k6 results are included in the final write-up.

---

## Q5: Web UI Automation

This project uses **Playwright with pytest** for automated end-to-end UI testing. The UI tests are located in:

```text
tests/ui/test_ui_flows.py
```

The suite includes five browser-based tests:

* Get Started button navigates from the home page to the login page
* New user registration with valid information
* Valid login and navigation to the polls list
* Invalid login displays an error message
* Unauthorized user is blocked from the Add Poll page

### Install Playwright Dependencies

```bash
python -m pip install pytest-playwright
python -m playwright install
```

### Run the Django Server

Before running the UI tests, start the Django app in one terminal:

```bash
python manage.py runserver
```

The app should be running at:

```text
http://127.0.0.1:8000/
```

### Run the UI Test Suite

In a second terminal, run:

```bash
python -m pytest tests/ui
```

### Optional: Run Tests with Browser Visible

```bash
python -m pytest tests/ui --headed
```

A successful run should show all five UI tests passing, with 5/5 greens.

```
```

## Q7: Integration Tests

The integration tests are located in:

tests/integration/test_poll_integration.py


Run the integration tests with:

```bash
python -m pytest tests/integration
```

---

## Current Project Structure

```text
.
├── accounts/
├── performance/
├── pollme/
├── polls/
├── reports/
│   ├── coverage/
│   ├── linter/
│   ├── performance/
│   ├── screenshots/
│   └── uat/
│       └── UAT_Test_suite.xlsx
├── tests/
│   └── unit/
│       ├── test_forms_unit.py
│       └── test_views_unit.py
├── manage.py
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## AI Use Disclosure

I used ChatGPT as a learning, planning, and debugging assistant for this project. Specifically, I used it to help interpret assignment requirements, organize the project structure, troubleshoot setup issues, understand how to configure Ruff and pytest, debug environment problems with pytest, and format parts of the README and write-up. I also used ChatGPT to help brainstorm how to describe test doubles such as dummy, stub, mock, and spy objects in the write-up.

The test execution, manual UAT results, screenshots, and final project decisions were reviewed and completed by me.

---

## References

* Django documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
* Pytest documentation: [https://docs.pytest.org/](https://docs.pytest.org/)
* pytest-django documentation: [https://pytest-django.readthedocs.io/](https://pytest-django.readthedocs.io/)
* pytest-cov documentation: [https://pytest-cov.readthedocs.io/](https://pytest-cov.readthedocs.io/)
* Ruff documentation: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)
* Original Django Poll App repository: [https://github.com/devmahmud/Django-Poll-App](https://github.com/devmahmud/Django-Poll-App)
* ChatGPT, used for assignment planning, debugging help, README formatting, and explanation of testing concepts