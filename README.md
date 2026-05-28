# Django Poll App QA Project

This repository contains my Software Quality Assurance final project for MPCS 56540. The project is based on an open-source Django Poll App and extends it with QA artifacts, including linting, user acceptance testing, unit tests, coverage reports, performance testing, UI automation, a smoke test plan, integration tests, code smell review, and CI/CD configuration.

## Reference Codebase

Original repository: https://github.com/devmahmud/Django-Poll-App

This repository contains my modified version of the app with added tests, reports, configurations, automation scripts, and project documentation.

---

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/sandyzhengg23/django-poll-qa-project.git
cd django-poll-qa-project
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
python -m pip install ruff pytest pytest-django pytest-cov pytest-playwright
python -m playwright install
```

Run database migrations:

```bash
python manage.py migrate
```

Optional: seed the database with sample data:

```bash
python seeder.py
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

## Q1: Linter / Static Review

This project uses **Ruff** for static analysis. Ruff is configured in:

```text
pyproject.toml
```

Run the linter:

```bash
ruff check .
```

Optional: save the linter output to a report file:

```bash
mkdir -p reports/linter
ruff check . > reports/linter/ruff_initial.txt || true
```

The linter/static review section in the final write-up includes five distinct examples of Ruff catching useful issues, including unused imports, long lines, unsorted imports, missing newline at end of file, and unused local variables.

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

The UAT suite covers major user-facing features of the Django Poll App, including:

* Viewing the public home page
* Navigating from Get Started to the login page
* Registering a new account
* Logging in with existing credentials
* Viewing the polls list
* Sorting polls by name, date, and vote count
* Searching polls
* Checking Add Poll permission behavior

The black-box testing techniques used include:

* Equivalence Partitioning
* Boundary Value Analysis
* State Transition Testing
* Decision Table Testing
* Pairwise Testing

Screenshots of the authored and executed UAT suite are included in the project write-up.

---

## Q3: Unit Tests

The unit tests are located in:

```text
tests/unit/
```

The unit test suite includes tests for form validation and view behavior. The tests use test doubles to isolate behavior from shared dependencies such as the database, authenticated user objects, Django messages, redirects, and vote persistence.

The test double types used include:

* Dummy
* Stub
* Mock
* Spy

### Run Unit Tests

```bash
python -m pytest tests/unit
```

### Run Unit Tests with Coverage

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

---

## Q4: Performance Testing

This project uses **k6** for performance testing. The performance test scripts are located in:

```text
performance/load_test.js
performance/spike_test.js
```

The two performance test types are:

* Load test: tests the app under normal expected traffic
* Spike test: tests the app under a sudden traffic increase

The tested endpoints include:

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

The suite includes browser-based tests for major user flows, such as:

* Navigating from the home page
* Registering a new user
* Logging in with valid credentials
* Displaying an error for invalid login
* Blocking unauthorized users from protected pages

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

---

## Q6: Smoke Test Plan

The smoke test plan is included in the final project write-up.

The smoke test plan defines what it means for a new build of the Django Poll App to be healthy enough for deeper testing. It covers the most critical user paths, including:

* Home page loading
* Get Started navigation
* User registration
* User login
* Invalid login rejection
* Polls list access

The smoke test plan includes:

* Objective
* Scope and coverage
* Approach
* Smoke test cases
* Test deliverables
* Environment and resources
* Schedule and entry/exit criteria
* Risks and contingency plans

This plan is a design deliverable and does not need to be executed as part of the automated test suite.

---

## Q7: Integration Tests

The integration tests are located in:

```text
tests/integration/
```

The integration tests exercise real boundaries between components, such as:

* Polls list view, database, and rendered template response
* Vote view, Poll model, Choice model, Vote model, and database

Run the integration tests with:

```bash
python -m pytest tests/integration
```

---

## Q8: Code Smells

The code smell review is included in the final project write-up.

The review identifies three different code smell types in the application source code:

* Duplicate Code
* Long Method
* Comments

For each code smell, the write-up includes:

* Code smell type
* File and line location
* Why it is a smell
* Proposed improvement
* Code excerpt showing the issue

This section is a review exercise, so the identified code smells were documented and analyzed rather than fully refactored.

---

## Q9: CI/CD Pipeline

This repository includes GitHub Actions workflow configuration in:

```text
.github/workflows/
```

The CI/CD pipeline is configured to automate quality checks such as:

* Setting up the application
* Running the linter
* Running unit tests
* Running integration tests
* Running performance tests
* Running UI automation tests

The final write-up includes screenshots of both:

* A successful pipeline run
* A failing pipeline run that demonstrates the lint or test gate working

---

## Run All Automated Tests

To run unit, UI, and integration tests together:

```bash
python -m pytest tests
```

To run all tests with coverage for the Django app code:

```bash
python -m pytest tests \
  --cov=accounts \
  --cov=polls \
  --cov-report=term-missing
```

---

## Current Project Structure

```text
.
├── .github/
├── accounts/
├── performance/
├── pollme/
├── polls/
├── reports/
├── static/
├── templates/
├── tests/
├── .gitignore
├── LICENSE
├── manage.py
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── requirements.txt.save
└── seeder.py
```

---

## AI Use Disclosure

I used ChatGPT as a learning, planning, and debugging tool while working on this project. Specifically, I used it to help interpret assignment requirements, organize the project structure, troubleshoot setup issues, understand how to configure Ruff and pytest, debug environment problems with pytest, debug errors that occurred during the coding process, and format parts of the README and write-up.

I also used ChatGPT to help understand CI/CD workflow syntax and to help format the GitHub Actions pipeline configuration. The test execution, manual UAT results, screenshots, and final project decisions were reviewed and completed by me.

---

## References

* Django documentation: https://docs.djangoproject.com/
* Pytest documentation: https://docs.pytest.org/
* pytest-django documentation: https://pytest-django.readthedocs.io/
* pytest-cov documentation: https://pytest-cov.readthedocs.io/
* Ruff documentation: https://docs.astral.sh/ruff/
* k6 documentation: https://grafana.com/docs/k6/latest/
* Playwright Python documentation: https://playwright.dev/python/
* GitHub Actions documentation: https://docs.github.com/en/actions
* Original Django Poll App repository: https://github.com/devmahmud/Django-Poll-App
* ChatGPT, used for assignment planning, debugging help, README formatting, CI/CD syntax help, and explanation of testing concepts
