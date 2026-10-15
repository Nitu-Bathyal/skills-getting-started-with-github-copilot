from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original_activities = deepcopy(activities)
    yield TestClient(app)
    activities.clear()
    activities.update(original_activities)


def test_get_activities_returns_sample_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert len(response.json()) == 9


def test_signup_rejects_duplicate_participant(client):
    email = "duplicate@example.com"

    first_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    second_response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_unregister_removes_participant(client):
    email = "remove@example.com"
    client.post(f"/activities/Chess%20Club/signup?email={email}")

    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]