from src.app import activities


def test_signup_adds_participant_when_request_is_valid(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {"email": " NewStudent@Mergington.edu "}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up successfully"}
    assert "newstudent@mergington.edu" in activities[activity_name]["participants"]


def test_signup_returns_409_for_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {"email": "MICHAEL@MERGINGTON.EDU"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "Student already signed up"


def test_signup_returns_404_when_activity_does_not_exist(client):
    # Arrange
    activity_name = "Unknown Club"
    payload = {"email": "student@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 422
