import pytest
from server import create_app, loadClubs
from flask_testing import TestCase
clubs = loadClubs()
all_emails = [club["email"] for club in clubs]


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_request_correct_login(client):
    response = response = client.get("/logout")
    assert response.status_code == 302
