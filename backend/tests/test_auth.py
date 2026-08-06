from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from backend.app import app
import routes.auth as auth_routes


@pytest.fixture
def client():
    previous_testing = app.config.get("TESTING")
    previous_jwt_secret = app.config.get("JWT_SECRET_KEY")

    app.config.update(
        TESTING=True,
        JWT_SECRET_KEY=(
            "test-only-jwt-secret-key-"
            "with-more-than-32-bytes"
        ),
    )

    try:
        with app.test_client() as test_client:
            yield test_client
    finally:
        app.config["TESTING"] = previous_testing
        app.config["JWT_SECRET_KEY"] = previous_jwt_secret

def test_register_creates_student_without_live_database(
    client,
    monkeypatch,
):
    users = MagicMock()
    users.find_one.return_value = None
    users.insert_one.return_value = SimpleNamespace(
        inserted_id="test-user-id"
    )

    monkeypatch.setattr(
        auth_routes,
        "users_collection",
        lambda: users,
    )
    monkeypatch.setattr(
        auth_routes,
        "append_registered_student",
        lambda **kwargs: {
            "email": kwargs["email"],
            "fullName": kwargs["full_name"],
        },
    )

    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "Test User",
            "email": "test@test.com",
            "password": "123456",
            "role": "student",
        },
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Registration Successful"

    users.insert_one.assert_called_once()
    inserted_user = users.insert_one.call_args.args[0]

    assert inserted_user["email"] == "test@test.com"
    assert inserted_user["role"] == "student"
    assert inserted_user["password"] != "123456"
    assert check_password_hash(
        inserted_user["password"],
        "123456",
    )


def test_login_returns_token_without_live_database(
    client,
    monkeypatch,
):
    users = MagicMock()
    users.find_one.return_value = {
        "fullName": "Test User",
        "email": "test@test.com",
        "username": "testuser",
        "password": generate_password_hash("123456"),
        "role": "student",
    }

    monkeypatch.setattr(
        auth_routes,
        "users_collection",
        lambda: users,
    )
    monkeypatch.setattr(
        auth_routes,
        "find_csv_user",
        lambda identifier, password: None,
    )
    monkeypatch.setattr(
        auth_routes,
        "find_workbook_user",
        lambda identifier, password: None,
    )
    monkeypatch.setattr(
        auth_routes,
        "legacy_imported_user",
        lambda identifier: None,
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["role"] == "student"
    assert data["user"]["email"] == "test@test.com"
    assert data["token"]