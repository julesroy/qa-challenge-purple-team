import pytest


def test_api_03(api_client):
    """Validation of employee details.

    HTTP Method & Endpoint:
        -> GET /web/index.php/api/v2/pim/employees/{empNumber}

    Preconditions:
        -> Authenticated session as Admin.
        -> An existing employee created with specified details.

    Parameters:
        -> Path param: empNumber

    Validates:
        -> HTTP status code is 200 OK.
        -> Content-Type header contains application/json.
        -> Response body data contains firstName and lastName matching injected values.
    """
    # prepare employee data for validation
    payload = {
        "firstName": "QA",
        "middleName": "Auto",
        "lastName": "Tester",
        "empPicture": None
    }

    emp_number = None
    try:
        # precondition: create employee record to validate
        create_resp = api_client.create_employee(payload)
        assert create_resp.status_code in [200, 201], (
            f"precondition failed: creation returned {create_resp.status_code}"
        )
        emp_number = create_resp.json().get("data", {}).get("empNumber")
        assert emp_number is not None, "precondition failed: empNumber not returned"

        # send get request to fetch details of created employee
        response = api_client.get_employee(emp_number)

        # verify http status code is 200 ok
        assert response.status_code == 200, f"expected status 200, got {response.status_code}"

        # verify content-type header
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"expected application/json, got {content_type}"

        # verify response body data matches injected attributes
        res_json = response.json()
        assert "data" in res_json, "response body missing 'data' key"
        emp_data = res_json["data"]

        assert emp_data.get("firstName") == payload["firstName"], (
            f"expected firstName {payload['firstName']}, got {emp_data.get('firstName')}"
        )
        assert emp_data.get("lastName") == payload["lastName"], (
            f"expected lastName {payload['lastName']}, got {emp_data.get('lastName')}"
        )
        assert str(emp_data.get("empNumber")) == str(emp_number), (
            f"expected empNumber {emp_number}, got {emp_data.get('empNumber')}"
        )
    finally:
        # clean up created employee record
        if emp_number:
            api_client.delete_employees([emp_number])
