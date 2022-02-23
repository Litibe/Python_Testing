import email
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

    # other setup can go here

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_correct_login(client):
    print(all_emails[0])
    params={"email":all_emails[0]}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 200

def test_request_incorrect_login(client):
    params={"email":"test@test.fr"}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 302
