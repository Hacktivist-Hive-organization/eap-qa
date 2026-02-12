import pytest
from test_data.constants.api_endpoints import RequestsEndpoints
import uuid
from pathlib import Path
import json

AUTO = object()
file_path = Path(__file__).parent / 'data'


def unique_request_title():
    return f"e2e_request_{uuid.uuid4().hex}"


@pytest.fixture(scope="session")
def request_payloads():
    return json.loads((file_path / "requests.json").read_text(encoding="utf-8"))


@pytest.fixture
def request_types(api_client, auth_headers):
    response = api_client.get(RequestsEndpoints.REQUEST_TYPES, headers=auth_headers)
    response.raise_for_status()
    return response.json()


@pytest.fixture
def request_types_map(request_types):
    type_name_to_id = {}
    subtype_by_type = {}
    for t in request_types:
        type_name = t["name"]
        type_name_to_id[type_name] = t["id"]
        subtype_by_type[type_name] = {st["name"]: st["id"] for st in t.get("subtypes", [])}

    return type_name_to_id, subtype_by_type


@pytest.fixture
def make_request(request_types_map, request_payloads):
    type_name_to_id, subtype_by_type = request_types_map
    default_scenario = "type1_request"

    def _make_request(
            *,
            scenario=AUTO,
            type_name=AUTO,
            subtype_name=AUTO,
            title=AUTO,
            description=AUTO,
            business_justification=AUTO,
            priority=AUTO,
    ):
        if scenario is AUTO:
            base = request_payloads[default_scenario]
        elif isinstance(scenario, str):
            base = request_payloads[scenario]
        else:
            base = scenario

        type_name = base["type"] if type_name is AUTO else type_name
        subtype_name = base["subtype"] if subtype_name is AUTO else subtype_name

        request = {
            "type_id": type_name_to_id[type_name],
            "subtype_id": subtype_by_type[type_name][subtype_name],
            "title": unique_request_title() if title is AUTO else title,
            "description": base.get("description") if description is AUTO else description,
            "business_justification": base.get(
                "business_justification") if business_justification is AUTO else business_justification,
            "priority": base.get("priority") if priority is AUTO else priority,
        }
        return request

    return _make_request


@pytest.fixture
def create_request(api_client, auth_headers, make_request):
    def _create_request():
        payload = make_request()
        response = api_client.post(RequestsEndpoints.REQUESTS, body=payload, headers=auth_headers)
        assert response.status_code == 200, response.text
        data = response.json()
        return data

    return _create_request
