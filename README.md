# pytest-qa-prep

![CI](https://github.com/SergeyTranin/pytest-qa-prep/actions/workflows/ci.yml/badge.svg)

A QA automation portfolio project built with **Python**, **pytest**, and **Playwright**.
It combines API test automation, UI test automation, and CI/CD to demonstrate
real-world test framework design rather than isolated exercises.

## Project structure

pytest-qa-prep/
├── .github/workflows/ci.yml # CI pipeline (lint + tests)
├── api/
│   ├── clients/            # HTTP client wrappers
│   ├── models/             # response schema models
│   └── tests/              # API test suite
├── ui/
│   ├── pages/              # Page Object Model classes
│   └── tests/              # UI test suite (Playwright)
├── config/
│   ├── settings.py         # environment-driven settings
│   └── .env.example
├── utils/
│   ├── data_factories.py   # test data factories, helpers
│   └── logger.py
├── docs/
│   ├── test_strategy.md
│   └── bugs_found.md       # test strategy, bug reports
├── legacy/
│   ├── test/
│   └── calculator.py       # original calculator exercise (kept for history)
├── conftest.py
├── pytest.ini / pyproject.toml
├── requirements.txt
├── Dockerfile
└── README.md

## Status
This project is actively being built out. Current focus: pytest fundamentals
(fixtures, parametrization, markers) on top of the legacy calculator suite,
before layering in API and UI automation.
## Installation
1. Clone the repository:
   ```bash
   git clone [github.com](https://github.com/SergeyTranin/pytest-qa-prep.git)
   cd pytest-qa-prep

2. Create and activate a virtual environment:
   ```bash
    python3 -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Copy .env.example to .env and adjust values if needed.


## Running the tests
1. Run the full suite:
    ```bash
    pytest

2. Run a specific layer:
   ```bash
    pytest api/tests      # API tests
    pytest ui/tests       # UI tests (Playwright)
    pytest legacy         # original calculator tests

3. Filter by marker:
   ```bash
    pytest -m smoke        # fast critical-path checks
    pytest -m regression   # full regression suite

## Legacy: calculator project
The project started as a simple calculator exercise (basic arithmetic operations with unit tests). That code and its tests now live under legacy/ and are still part of the CI run — kept as a record of the project's starting point rather than deleted.

## Roadmap
 Repo structure + CI bootstrap
 API test suite (client layer, schema validation, negative cases)
 UI test suite (Page Object Model, Playwright)
 Hybrid API-seeds / UI-verifies tests
 Allure reporting + Dockerized CI pipeline