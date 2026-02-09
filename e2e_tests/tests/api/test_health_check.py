import pytest
from test_data.constants.api_endpoints import HealthEndpoints


@pytest.mark.api
def test_health_check(api_client):
    response = api_client.get(HealthEndpoints.HEALTH)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"
