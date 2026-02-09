import pytest
from test_data.constants.api_endpoints import AuthEndpoints, UserEndpoints
from test_data.fixtures.auth_fixtures import decode_token


@pytest.mark.api
def test_successful_login_with_valid_credentials(make_user, api_client, registered_user):
    user = registered_user
    login_payload = {"email": user["email"], "password": user["password"]}
    response = api_client.post(AuthEndpoints.LOGIN, body=login_payload)
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    payload = decode_token(body["access_token"])
    assert "sub" in payload
    assert "exp" in payload

    assert isinstance(body["access_token"], str)
    assert body["token_type"] == "bearer"

    assert body["user"]["email"] == user["email"]
    assert body["user"]["is_active"] is True
    assert "id" in body["user"]


@pytest.mark.api
def test_user_login_with_non_existing_email(make_user, api_client, registered_user):
    login_payload = {"email": "not-exist@example.com", "password": "Psd!1234"}
    response = api_client.post(AuthEndpoints.LOGIN, body=login_payload)
    assert response.status_code == 401
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Invalid email or password"


@pytest.mark.api
def test_login_with_wrong_password(api_client, registered_user):
    user = registered_user
    login_payload = {"email": user["email"], "password": "Wrong_password"}
    response = api_client.post(AuthEndpoints.LOGIN, body=login_payload)
    assert response.status_code == 401
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Invalid email or password"


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        ({"password": "Password123!"}),
        ({"email": "test@example.com"}),
    ],
)
def test_login_with_missing_email_password(api_client, payload):
    response = api_client.post(AuthEndpoints.LOGIN, body=payload)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body


@pytest.mark.api
def test_unauthorized_user_cannot_access_protected_endpoint(api_client):
    response = api_client.get(UserEndpoints.USERS_ME)
    assert response.status_code == 401
    body = response.json()
    assert "detail" in body


@pytest.mark.api
def test_authorized_user_access_protected_endpoint(api_client, auth_headers):
    response = api_client.get(UserEndpoints.USERS_ME, headers=auth_headers)
    assert response.status_code == 200
