import pytest


def test_api_04(api_client):
    """Deletion of an employee.

    HTTP Method & Endpoint:
        -> DELETE /web/index.php/api/v2/pim/employees

    Preconditions:
        -> Authenticated session as Admin.
        -> An existing employee to delete.

    Parameters:
        -> Body: {"ids": [<empNumber>]}

    Validates:
        -> HTTP status code is 200 OK.
        -> Deletion response body confirms deleted employee id.
        -> Subsequent GET request returns error status (404 or 422), confirming resource deletion.
    """
    # prepare employee creation payload for deletion test
    payload = {
        "firstName": "QA",
        "middleName": "Auto",
        "lastName": "Tester",
        "empPicture": None
    }

    # create employee to delete
    create_resp = api_client.create_employee(payload)
    assert create_resp.status_code in [200, 201], (
        f"precondition failed: creation returned {create_resp.status_code}"
    )
    emp_number = create_resp.json().get("data", {}).get("empNumber")
    assert emp_number is not None, "precondition failed: empNumber not returned"

    # send delete request with employee id
    delete_resp = api_client.delete_employees([emp_number])

    # verify http status code is 200 ok
    assert delete_resp.status_code == 200, f"expected status 200, got {delete_resp.status_code}"

    # verify deletion confirmation in response body
    del_json = delete_resp.json()
    assert "data" in del_json, "deletion response missing 'data' key"
    deleted_ids = [str(x) for x in del_json["data"]]
    assert str(emp_number) in deleted_ids, (
        f"expected empNumber {emp_number} in deleted ids {deleted_ids}"
    )

    # verify subsequent get request confirms deletion
    verify_resp = api_client.get_employee(emp_number)
    assert verify_resp.status_code in [404, 422], (
        f"expected status 404 or 422 after deletion, got {verify_resp.status_code}"
    )
