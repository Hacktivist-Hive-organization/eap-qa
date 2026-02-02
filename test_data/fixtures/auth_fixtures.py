import pytest
import logging
import uuid

logger = logging.getLogger("fixture_logger")

# returns a new featureless instance
AUTO = object()

def unique_email() -> str:
    return f"e2e_{uuid.uuid4().hex}@example.com"


def invalid_email() -> str:
    return f"e2e_{uuid.uuid4().hex}not-a-valid-email"


def strong_password() -> str:
    return f"Pw!{uuid.uuid4().hex}"


def weak_passwords():
    return {
        "too_short": "Ab!1",
        "only_lower": uuid.uuid4().hex.lower(),
        "only_upper": uuid.uuid4().hex.upper(),
        "alphanumeric": f"Ab{uuid.uuid4().hex}",
    }


@pytest.fixture
def make_user():
    # to track test data
    users = []

    def _make_user(
            email= AUTO,
            password= AUTO,
            first_name= AUTO,
            last_name= AUTO,
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
