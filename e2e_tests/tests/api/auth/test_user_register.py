import pytest
from test_data.constants.api_endpoints import AuthEndpoints
from test_data.fixtures.auth_fixtures import weak_passwords, invalid_email, decode_token

REGISTER_URL = AuthEndpoints.REGISTER


@pytest.mark.api
def test_register_with_new_user(make_user, api_client):
    user = make_user()
    response = api_client.post(REGISTER_URL, body=user)
    assert response.status_code == 201

    body = response.json()
    assert "access_token" in body
    payload = decode_token(body["access_token"])
    assert "sub" in payload
    assert "exp" in payload

    assert isinstance(body["access_token"], str)
    assert body["token_type"] == "bearer"

    assert body["user"]["email"] == user["email"]
    assert body["user"]["first_name"] == user["first_name"]
    assert body["user"]["last_name"] == user["last_name"]
    assert "id" in body["user"]


@pytest.mark.api
def test_register_with_existing_user(make_user, api_client):
    user = make_user()
    response1 = api_client.post(REGISTER_URL, body=user)
    assert response1.status_code == 201

    response2 = api_client.post(REGISTER_URL, body=user)
    assert response2.status_code == 409
    body = response2.json()
    assert "detail" in body
    assert body["detail"] == "User already exists"


@pytest.mark.api
def test_register_with_invalid_email(make_user, api_client):
    user = make_user(email=invalid_email())
    response = api_client.post(REGISTER_URL, body=user)
    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Invalid email or password"


@pytest.mark.api
@pytest.mark.parametrize("pw", list(weak_passwords().values()))
def test_register_with_weak_password(make_user, api_client, pw):
    user = make_user(password=pw)
    response = api_client.post(REGISTER_URL, body=user)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Password is too weak"


@pytest.mark.api
@pytest.mark.parametrize(
    "overrides",
    [
        ({"email": ""}),
        ({"email": "   "}),
        ({"password": ""}),
        ({"password": "   "}),
        ({"first_name": ""}),
        ({"first_name": "   "}),
        ({"last_name": ""}),
        ({"last_name": "   "}),
    ],
)
def test_register_with_blank_or_null_fields(make_user, api_client, overrides):
    user = make_user(**overrides)
    response = api_client.post(REGISTER_URL, body=user)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "All required fields must be filled"


@pytest.mark.api
@pytest.mark.parametrize("missing_field", ["email", "password", "first_name", "last_name"])
def test_register_missing_required_fields(make_user, api_client, missing_field):
    user = make_user()
    user.pop(missing_field)
    response = api_client.post(REGISTER_URL, body=user)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
