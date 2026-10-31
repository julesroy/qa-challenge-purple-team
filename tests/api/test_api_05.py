import pytest


def test_api_05(api_client):
    """Creation with incomplete payload.

    HTTP Method & Endpoint:
        -> POST /web/index.php/api/v2/admin/users

    Preconditions:
        -> Authenticated session as Admin.

    Parameters:
        -> Body: {} (empty payload)

    Validates:
        -> HTTP status code is 422 Unprocessable Entity or 400 Bad Request.
        -> Response body contains client error details and identifies missing required fields.
    """
    # send post request with empty body to user creation endpoint
    response = api_client.post("/web/index.php/api/v2/admin/users", json={})

    # verify client error status code (422 or 400)
    assert response.status_code in [400, 422], (
        f"expected status 400 or 422 for empty payload, got {response.status_code}"
    )

    # verify error details in response body
    res_json = response.json()
    assert "error" in res_json, "response json missing 'error' object"
    error_obj = res_json["error"]

    # verify error message or invalid param details
    assert "message" in error_obj or "data" in error_obj, "error object missing message or data"

    # verify missing required fields are reported by api
    invalid_keys = error_obj.get("data", {}).get("invalidParamKeys", [])
    expected_missing = ["username", "password", "userRoleId", "empNumber", "status"]
    has_expected_field = any(field in invalid_keys for field in expected_missing) or "Invalid" in error_obj.get("message", "")
    assert has_expected_field, f"expected invalid keys among {expected_missing}, got {invalid_keys}"
