import pytest


def test_api_02(api_client):
    """Creation of a new employee.

    HTTP Method & Endpoint:
        -> POST /web/index.php/api/v2/pim/employees

    Preconditions:
        -> Authenticated session as Admin.

    Parameters:
        -> Body: {"firstName": "QA", "middleName": "Auto", "lastName": "Tester", "empPicture": null}

    Validates:
        -> HTTP status code is 200 OK (or 201 Created).
        -> Response body data contains assigned empNumber.
        -> Response body data matches firstName 'QA'.
    """
    # prepare employee creation payload
    payload = {
        "firstName": "QA",
        "middleName": "Auto",
        "lastName": "Tester",
        "empPicture": None
    }

    emp_number = None
    try:
        # send post request to create employee
        response = api_client.create_employee(payload)

        # verify http status code indicates success
        assert response.status_code in [200, 201], f"expected status 200 or 201, got {response.status_code}"

        # verify response payload structure and returned fields
        res_json = response.json()
        assert "data" in res_json, "response body missing 'data' key"
        data = res_json["data"]

        # store and verify generated empnumber
        emp_number = data.get("empNumber")
        assert emp_number is not None, "data.empNumber was not returned"

        # verify firstname and lastname match submitted values
        assert data.get("firstName") == payload["firstName"], (
            f"expected firstName {payload['firstName']}, got {data.get('firstName')}"
        )
        assert data.get("lastName") == payload["lastName"], (
            f"expected lastName {payload['lastName']}, got {data.get('lastName')}"
        )
    finally:
        # clean up created employee to ensure test independence
        if emp_number:
            api_client.delete_employees([emp_number])
