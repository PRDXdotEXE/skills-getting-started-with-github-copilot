from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_available_activities():
    # Arrange
    expected_activity = "Art Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_activity in activities
    assert len(activities) >= 4


def test_signup_adds_participant_to_activity():
    # Arrange
    activity = "Art Club"
    email = "signup-test@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    client.delete(f"/activities/{activity}/signup", params={"email": email})


def test_unregister_removes_participant_from_activity():
    # Arrange
    activity = "Art Club"
    email = "unregister-test@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unknown_activity_returns_not_found():
    # Arrange
    activity = "Unknown Activity"

    # Act
    response = client.get(f"/activities/{activity}")

    # Assert
    assert response.status_code == 404