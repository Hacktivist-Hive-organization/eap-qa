import pytest


@pytest.mark.api
def test_health_check(api_client):
    response = api_client.get("/api/v1/health/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"


def test_register_new_user():
    pass