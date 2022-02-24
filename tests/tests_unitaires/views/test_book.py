import email
import pytest
from server import create_app, loadClubs, loadCompetitions

clubs = loadClubs()
competitions = loadCompetitions()


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


def test_render_context_showSummary_clubs_details(client):
    club = clubs[0]
    club_name = club["name"].split(" ")
    competition = competitions[0]
    competition_name = competition["name"].split(" ")

    url = "/book/" + competition_name[0]+"%20"+competition_name[1] + "/"
    url += club_name[0]+"%20"+club_name[1]
    response = client.get(url)
    assert response.status_code == 200
    assert ("Places available: " +
            competition['numberOfPlaces']).encode() in response.data
