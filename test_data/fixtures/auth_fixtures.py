import pytest
import logging
import uuid
from jose import jwt
from test_data.constants.api_endpoints import AuthEndpoints

logger = logging.getLogger("fixture_logger")

# returns a new featureless instance
AUTO = object()
REGISTER_URL = AuthEndpoints.REGISTER
LOGIN_URL = AuthEndpoints.LOGIN

def unique_email() -> str:
    return f"e2e_{uuid.uuid4().hex}@example.com"


def invalid_email() -> str:
    return f"e2e_{uuid.uuid4().hex}not-a-valid-email"


def strong_password() -> str:
    return f"Pw!{uuid.uuid4().hex}"


def weak_passwords() -> dict:
    return {
        "too_short": "Ab!1",
        "only_lower": uuid.uuid4().hex.lower(),
        "only_upper": uuid.uuid4().hex.upper(),
        "alphanumeric": f"Ab{uuid.uuid4().hex}",
    }


def decode_token(access_token: str) -> dict:
    decoded_payload = jwt.decode(
        access_token,
        key="",
        options={
            "verify_signature": False,
            "verify_exp": False,
        },
    )
    return decoded_payload


@pytest.fixture
def make_user():
    # to track test data
    users = []

    def _make_user(
            email=AUTO,
            password=AUTO,
            first_name=AUTO,
            last_name=AUTO,
    ):
        user = {
            "email": unique_email() if email is AUTO else email,
            "password": strong_password() if password is AUTO else password,
            "first_name": "Test" if first_name is AUTO else first_name,
            "last_name": "User" if last_name is AUTO else last_name,
        }
        users.append(user)
        logger.info("Created user email=%r", user["email"])
        return user

    yield _make_user


@pytest.fixture
def registered_user(make_user, api_client) -> dict:
    user = make_user()
    response = api_client.post(REGISTER_URL, body=user)
    assert response.status_code == 201
    return user


@pytest.fixture
def access_token(api_client, registered_user):
    response = api_client.post(LOGIN_URL, body=registered_user)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}