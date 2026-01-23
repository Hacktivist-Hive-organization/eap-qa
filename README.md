# EAP Project Test Automation and QA Documentation
EAP project uses Playwright and pytest testing framework and GitHub Actions for continuous integration.

## Installation
1) Clone eap-qa repository
2) Install virtual environment -> python -m venv .venv
3) Activate virtual environment -> source .venv/bin/activate
4) Install dependencies ->  pip install -r requirements.txt
5) Install browsers -> playwright install
6) You can run the tests with using markers (api, ui, regression).
    >> pytest -m api
