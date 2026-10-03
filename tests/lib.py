# tests/lib.py

from fastapi.testclient import TestClient
from data.user_data import user_list


def seed_db(db):
    db.commit()
    db.add_all(user_list)
    db.commit()


def login(test_app: TestClient, email: str, password: str):
    # Log in using an existing mock user
    response = test_app.post(
        "/api/login",
        json={
            "email": email,
            "password": password
        }
    )

    if response.status_code != 201:
        raise Exception(
            f"Login failed: {response.json().get('detail', 'Unknown error')}"
        )

    token = response.json().get("token")

    if not token:
        raise Exception("No token returned from login endpoint.")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers