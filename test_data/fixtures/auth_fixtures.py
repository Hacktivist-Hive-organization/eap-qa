import pytest
import logging
import uuid

logger = logging.getLogger("fixture_logger")


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
            email: str | None = None,
            password: str | None = None,
            first_name: str = "Test",
            last_name: str = "User"
    ):
        user = {
            "email": unique_email() if email is None else email,
            "password": strong_password() if password is None else password,
            "first_name": first_name,
            "last_name": last_name
        }
        users.append(user)
        logger.info("Created user email=%r", user["email"])
        return user

    yield _make_user
   #logger.info(f"Cleanup: {len(users)} users")
