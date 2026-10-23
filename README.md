# qa-challenge-purple-team

Tested website : https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index

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
├── tests/
│   ├── ui/ # UI tests
│   │   └── test_login.py # login test example
│   ├── api/ # API tests
│   └── to complete
│
├── pages/ # pages
│   ├── login_page.py
│   └── to complete
│
├── data/ # data files
│   ├── to complete
│
├── logs/ # logs
│   ├── ui_tests.log
│   └── api_tests.log
│
├── conftest.py # test configuration 
├── pytest.ini # pytest configuration
├── requirements.txt # python dependencies
└── reports/ # test execution reports
    └── report.html
```

## 1. Tests UI Automation (Selenium)

| Test ID | Test Name | Test Type | Preconditions | Test Data | Execution Steps | Expected Results | Assertions / Validations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST-UI-01** | Successful login to application | Positive / Smoke | Login page accessible | `username: "Admin"`, `password: "admin123"` | 1. Enter username. 2. Enter password. 3. Click Login. | Redirection to main dashboard. | URL contains `/dashboard/index` and dashboard heading is visible. |
| **TEST-UI-02** | Login failure with invalid password | Negative / Validation | Login page accessible | `username: "Admin"`, `password: "BadPassword999"` | 1. Enter username. 2. Enter invalid password. 3. Click Login. | Login fails, alert message displayed. | No redirection and element `.oxd-alert-content-text` is visible with text "Invalid credentials". |
| **TEST-UI-03** | Employee creation with profile picture | Positive / Upload | Logged in as Admin | `firstName: "John"`, `lastName: "Doe"`, `file: "avatar.jpg"` | 1. Navigate to PIM > Add Employee. 2. Enter first and last name. 3. Upload image to file input. 4. Save. | Employee created successfully and avatar displayed. | "Successfully Saved" success toast displayed and redirection to created profile. |
| **TEST-UI-04** | Add attachment to employee profile | Positive / File validation | Logged in, employee profile open | `file: "contract.pdf"`, `comment: "Employment contract"` | 1. Scroll to Attachments section. 2. Click Add. 3. Select PDF file. 4. Enter comment. 5. Save. | Document is attached to profile and listed. | Attachments table displays a new row containing "contract.pdf". |
| **TEST-UI-05** | Reject unauthorized file upload | Negative / Failure-oriented | Logged in, upload modal open | `file: "script_payload.exe"` | 1. Open attachment upload form. 2. Upload .exe file. 3. Submit. | System blocks unsupported file. | Error message visible `.oxd-input-field-error-message` and file is not saved. |
| **TEST-UI-06** | Personal details update | Positive / State verification | Logged in as Admin | `nationality: "French"`, `maritalStatus: "Single"`, `dob: "1995-05-12"` | 1. Navigate to My Info. 2. Select nationality from dropdown. 3. Choose marital status. 4. Select date in date picker. 5. Save. | Modified data is saved and persisted. | "Successfully Updated" toast displayed and inputs retain selected values. |
| **TEST-UI-07** | Pay grade boundary validation | Boundary testing | Logged in, on Admin > Job > Pay Grades | `currency: "Euro"`, `minSalary: 50000`, `maxSalary: 30000` | 1. Add currency to Pay Grade. 2. Enter minimum salary higher than maximum salary. 3. Trigger validation. | System prevents minimum value higher than maximum. | Inline error message "Should be higher than Minimum Salary" is visible. |
| **TEST-UI-08** | Delete user via modal confirmation | Dialog handling / Dynamic | Logged in, test user exists | `searchUsername: "test.user"` | 1. Navigate to Admin > User Management. 2. Search for user. 3. Click trash icon. 4. Confirm on "Yes, Delete" modal. | Modal closes and user is removed from list. | Confirmation modal intercepted and deleted item disappears from table. |
| **TEST-UI-09** | Leave request with date validation | Positive / Date validation | Logged in, leave balance available | `leaveType: "CAN - Vacation"`, `fromDate: "2026-11-10"`, `toDate: "2026-11-12"` | 1. Navigate to Leave > Apply. 2. Select leave type. 3. Select start and end dates. 4. Fill in comment. 5. Submit. | Request is submitted with correct status. | Success message displayed and request listed in Leave > My Leave as "Pending Approval". |
| **TEST-UI-10** | Multiple user creation via dataset | Data-driven testing | Logged in as Admin, CSV/JSON file ready | 3 rows of data: roles, statuses, credentials | 1. Loop via DataProvider / Parameterized runner. 2. Open add user form. 3. Fill with current row data. 4. Save. | 3 distinct users are created sequentially. | Success on each iteration and presence of all 3 accounts in Admin list. |

---

## 2. Tests API Automation

| Test ID | Test Name | HTTP Method & Endpoint | Test Type | Preconditions | Parameters / Payload | Expected HTTP Status | Assertions / Validations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST-API-01** | Retrieve user list | `GET /web/index.php/api/v2/admin/users` | Status / Schema / Headers | Authenticated session (Cookie / Token) | `limit=10`, `offset=0` | `200 OK` | `Content-Type` contains `application/json`, body contains a non-empty `data` array. |
| **TEST-API-02** | Create a new employee | `POST /web/index.php/api/v2/pim/employees` | CRUD (Create) | Valid authenticated session | Body: `{"firstName": "QA", "middleName": "Auto", "lastName": "Tester", "empPicture": null}` | `200 OK` or `201 Created` | Field `data.empNumber` is returned and `data.firstName` equals "QA". ID is stored. |
| **TEST-API-03** | Validate employee details | `GET /web/index.php/api/v2/pim/employees/{empNumber}` | Data validation | Employee created via TEST-API-02 | Path param: `empNumber` from TEST-API-02 | `200 OK` | Keys `firstName` and `lastName` in response match injected values. |
| **TEST-API-04** | Delete an employee | `DELETE /web/index.php/api/v2/pim/employees` | CRUD (Delete) | Employee to delete exists | Body: `{"ids": [<empNumber>]}` | `200 OK` | Deletion confirmation in body, and subsequent GET returns `404 Not Found`. |
| **TEST-API-05** | Creation with incomplete payload | `POST /web/index.php/api/v2/admin/users` | Negative / Error validation | Valid authenticated session | Body: `{}` (empty payload) | `422 Unprocessable Entity` or `400 Bad Request` | HTTP status indicates client error and JSON details missing fields. |

---

## 3. Tests reporting 

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
On macOS :
```bash
open reports/report.html
```

On Linux :
```bash
xdg-open reports/report.html
```

On Windows :
```bash
start reports/report.html
```