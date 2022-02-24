import pytest
from server import create_app

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
    assert b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in response.data
    assert response.status_code == 200