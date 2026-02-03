import pytest

HEALTH_URL = "/api/v1/health/"


@pytest.mark.api
def test_health_check(api_client):
    response = api_client.get(HEALTH_URL)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"
