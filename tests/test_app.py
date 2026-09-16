from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"
    encoded_activity = quote(activity_name)
    encoded_email = quote(email)

    activity = activities[activity_name]
    if email not in activity["participants"]:
        activity["participants"].append(email)

    response = client.delete(f"/activities/{encoded_activity}/participants?email={encoded_email}")

    assert response.status_code == 200
    assert email not in response.json()["participants"]
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Basketball Team"
    email = "missing.student@mergington.edu"
    encoded_activity = quote(activity_name)
    encoded_email = quote(email)

    response = client.delete(f"/activities/{encoded_activity}/participants?email={encoded_email}")

    assert response.status_code == 404
