import pytest
from server import create_app, loadClubs

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


def test_request_index(client):
    response = client.get("/")
    elementhtml = "<h1>Welcome to the GUDLFT Registration Portal!</h1>"
    assert elementhtml.encode() in response.data
    assert response.status_code == 200


def test_request_correct_login(client):
    params = {"email": all_emails[0]}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 200


def test_request_incorrect_login(client):
    params = {"email": "test@test.fr"}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 302


def test_request_correct_login(client):
    response = response = client.get("/logout")
    assert response.status_code == 302


def test_render_context_showSummary_clubs_details(client):
    clubs = loadClubs()
    response = client.post(
        "/showSummary", data={"email":  clubs[0]['email']})
    assert response.status_code == 200
    assert ("Points available: "+clubs[0]['points']).encode() in response.data
    assert clubs[0]['email'].encode() in response.data
