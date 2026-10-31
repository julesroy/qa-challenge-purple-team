import pytest


def test_api_01(api_client):
    """Fetch user list.

    HTTP Method & Endpoint:
        -> GET /web/index.php/api/v2/admin/users

    Preconditions:
        -> Authenticated session as Admin.

    Parameters:
        -> Query params: limit=10, offset=0

    Validates:
        -> HTTP status code is 200 OK.
        -> Content-Type header contains application/json.
        -> Response body contains a non-empty data array.
        -> First user record contains essential schema fields (id, userName).
    """
    # send get request to retrieve users with pagination parameters
    response = api_client.get_users(limit=10, offset=0)

    # verify http status code is 200 ok
    assert response.status_code == 200, f"expected status 200, got {response.status_code}"

    # verify content-type header contains application/json
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"expected application/json in header, got {content_type}"

    # parse response json body
    res_json = response.json()

    # verify data field exists and is a non-empty list
    assert "data" in res_json, "response body missing 'data' key"
    users = res_json["data"]
    assert isinstance(users, list), "response 'data' must be a list"
    assert len(users) > 0, "response 'data' list should not be empty"

    # verify schema structure on the first returned user item
    first_user = users[0]
    assert "id" in first_user, "user record missing 'id' field"
    assert "userName" in first_user or "username" in first_user, "user record missing username field"
