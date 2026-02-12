# EAP QA – Test Automation & CI Documentation
This repository contains automated **API** and **UI (End-to-End)** tests for the EAP project.

The project uses:

- **pytest** – Test framework  
- **Playwright** – UI automation   
- **GitHub Actions** – Continuous Integration  
---

# 📦 Project Structure
```
e2e_tests/
│
├── api/ # API client & helpers
├── tests/
│ ├── api/ # API test cases
│ └── ui/ # Playwright UI tests
├── ui/ # Page objects / UI helpers
├── utils/ # Config & utility functions
└── conftest.py # Shared pytest configuration
test_data/
│
├── constants/ # API endpoint definitions
└── fixtures/ # Pytest fixture factories
```

## Installation
1) Clone eap-qa repository
2) Install virtual environment
    >> python -m venv .venv
3) Activate virtual environment 
    >> source .venv/bin/activate
4) Install dependencies 
    >>  pip install -r requirements.txt
5) Install browsers 
    >> playwright install

# 🧪 Running Tests

 Tests are grouped using pytest markers:

| Marker       | Description           |
| ------------ | --------------------- |
| `api`        | Backend API tests     |
| `ui`         | Playwright UI tests   |

 You can run the tests with using markers (api, ui).
 >> pytest -m api
 
 >> pytest -m ui
 

# 🎭 Playwright Traces (UI Debugging)
When UI tests run, Playwright traces are automatically generated. Each test produces a .zip trace file.

They are stored inside:

**artifacts/traces/**

# 🔍 How to Open a Trace Locally

>> playwright show-trace artifacts/traces/<trace-file>.zip

This opens the Playwright Trace Viewer in your browser.

You can inspect:

- Screenshots

- Network requests

- Console logs

- DOM snapshots

This is the primary debugging tool for failed UI tests.

# 🤖 CI (GitHub Actions)

UI and API tests are executed automatically:

- On scheduled nightly runs (weekdays at midnight)

- When manually triggered from GitHub Actions via Run Workflow button.

# 🔄 CI Workflow Overview

The CI pipeline performs the following steps:

1) Starts PostgreSQL service

2) Clones backend repository

3) Create schema and Runs database migrations

4) Installs backend dependencies and Starts backend server

5) Clones frontend repository

6) Starts frontend server

7) Installs test dependencies

8) Runs all tests

9) Uploads test artifacts includes HTML test report and Playwright trace files

# 📦 Accessing CI Test Results

If a test fails in CI:

1. Go to GitHub → Actions

2. Open the failed workflow run

3. Scroll to Artifacts

4. Download the artifacts package

Inside you will find: pytest-report.html and playwright traces zip files.