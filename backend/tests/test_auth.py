import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_register(client):

    response = client.post(

        "/api/auth/register",

        json={

            "fullName":"Test User",

            "email":"test@test.com",

            "password":"123456",

            "role":"student"

        }

    )

    assert response.status_code in [201,409]


def test_login(client):

    response = client.post(

        "/api/auth/login",

        json={

            "email":"test@test.com",

            "password":"123456"

        }

    )

    assert response.status_code == 200

    data=response.get_json()

    assert "token" in data