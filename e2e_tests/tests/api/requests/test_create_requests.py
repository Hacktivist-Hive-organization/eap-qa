import pytest
from test_data.constants.api_endpoints import RequestsEndpoints


@pytest.mark.api
@pytest.mark.parametrize("scenario_name", [
    "type1_request",
    "type2_request",
    "type3_request",
])
def test_create_draft_requests_with_different_types(api_client, auth_headers, make_request, scenario_name) -> None:
    payload = make_request(scenario=scenario_name)
    response = api_client.post(RequestsEndpoints.REQUESTS, body=payload, headers=auth_headers)
    assert response.status_code == 201, f"scenario={scenario_name} sent={payload} resp={response.text}"


@pytest.mark.api
def test_get_request_details_by_id(api_client, auth_headers, create_request):
    created = create_request()
    request_id = created["id"]
    endpoint = RequestsEndpoints.REQUEST_BY_ID.format(request_id=request_id)
    response = api_client.get(endpoint, headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    expected_keys = {
        "id", "title", "priority", "current_status", "description", "business_justification", "type", "subtype",

    }
    assert expected_keys.issubset(data.keys()), f"missing={expected_keys - set(data.keys())}"
    assert "requester" in data, f"requester missing: {data.keys()}"
    assert "id" in data["requester"]
    assert "email" in data["requester"]


@pytest.mark.api
@pytest.mark.parametrize(
    "name,overrides,code",
    [
        ("title too short", {"title": "abcd"}, 422),
        ("title too long", {"title": "x" * 201}, 422),
        ("desc too short", {"description": "x" * 19}, 422),
        ("desc too long", {"description": "x" * 2001}, 422),
        ("business just too short", {"business_justification": "x" * 19}, 422),
        ("business just too long", {"business_justification": "x" * 1001}, 422),
        ("invalid priority", {"priority": "urgent"}, 422),
    ]
)
def test_create_request_field_validation(api_client, auth_headers, make_request, name, overrides, code):
    payload = make_request(**overrides)
    resp = api_client.post(RequestsEndpoints.REQUESTS, body=payload, headers=auth_headers)
    assert resp.status_code == code, f"{name}: sent={payload} resp={resp.text}"
