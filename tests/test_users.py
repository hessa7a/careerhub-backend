from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import UserModel
from tests.lib import login


def test_register_user(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    # Data for registering a new user
    user_data = {
        "name": "Register Test User",
        "email": "register-test@example.com",
        "phone": "33333333",
        "password": "mys3cretp2ssw0rd",
        "role": "applicant",
    }

    # Send a POST request to register the user
    response = test_app.post("/api/register", json=user_data)

    # Verify that registration succeeds and returns a token
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["token"], str)
    assert data["token"]
    assert data["message"] == "Login successful"

    # Verify the user was created in the database
    user = (
        test_db.query(UserModel)
        .filter(UserModel.email == user_data["email"])
        .first()
    )

    assert user is not None
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
    assert user.phone == user_data["phone"]
    assert user.role == user_data["role"]


def test_get_current_user(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    # Create a new mock user in the test database
    user = UserModel(
        name="Current User",
        email="current-user@example.com",
        phone="44444444",
        role="applicant",
    )

    user.set_password("mys3cretp2ssw0rd")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    # Use the login helper to generate authentication headers
    headers = login(
        test_app,
        "current-user@example.com",
        "mys3cretp2ssw0rd"
    )

    # Send a GET request for the authenticated user
    response = test_app.get("/api/current_user", headers=headers)

    # Verify the response contains the correct user
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["name"] == user.name
    assert data["email"] == user.email