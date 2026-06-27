import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(app_module.activities)
    app_module.activities = copy.deepcopy(original_activities)
    yield
    app_module.activities = copy.deepcopy(original_activities)


def test_duplicate_signup_is_rejected():
    client = TestClient(app_module.app)

    first_response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert first_response.status_code == 200

    second_response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()

    activity = app_module.activities["Chess Club"]
    assert activity["participants"].count("test@example.com") == 1


def test_duplicate_signup_is_rejected_case_insensitively():
    client = TestClient(app_module.app)

    first_response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert first_response.status_code == 200

    second_response = client.post("/activities/Chess%20Club/signup?email=Test@Example.com")
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()
