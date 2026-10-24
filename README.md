# qa-challenge-purple-team

## Purple Team :

Members :
- MACAJONE Enzo
- ROY Jules
- TOUNSI Aymane-Adam
- VÉNIER Bastien
- VILARINHO Fabio

## Tested platform :

Tested website : https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index
It's an open-source Human Resource Management (HRM) system.

## Language / Dependencies :

To build our testing framework, we chose to use Python and these following dependencies :

- selenium : for UI automation
- requests : for API automation
- pytest : for test orchestration and reporting
- pytest-xdist : for parallel test execution
- pytest-html : for test execution reports
- pdoc : for framework documentation

## Installation :

On macOS / Linux :
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows :
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Structure :

We adopted a Page Object Model (POM) pattern for the UI automation part.

```
qa-challenge-purple-team/
│
├── .venv/ # virtual env
│
├── data/ # data files
│   ├── avatar.jpg
│   ├── contract.pdf
│   ├── script_payload.exe
│   └── users.csv
│
├── docs/ # codebase documentation
│   ├── pages/
│   ├── tests/
│   └── index.html
│
├── pages/ # pages
│   ├── login_page.py
│   └── ...
│
├── reports/ # reports
│   └── report.html
│
├── tests/
│   ├── ui/ # UI tests
│   │   ├── test_ui_01.py
│   │   └── ...
│   └── api/ # API tests
│
├── conftest.py # test configuration
├── Purple_Team_Test_case_documentation.docx # test case documentation
├── pytest.ini # pytest configuration
└── requirements.txt # python dependencies
```

## Tests reporting :

Reports are generated automatically in the `reports/` directory using `pytest-html`.

### Run tests and generate report :
```bash
# Run all tests (the report is generated in reports/report.html)
pytest

# Run only UI tests
pytest tests/ui

# Run only API tests
pytest tests/api
```

### View report :

Then open reports/report.html in your browser.

### Documentation :
To generate documentation, we use `pdoc` :
```bash
pdoc -o docs/ pages/ tests/
```

Then you can open index.html in the docs/ directory to access codebase documentation.