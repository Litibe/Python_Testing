import datetime
import pytest
from server import create_app, load_datime_now, loadClubs, loadCompetitions, saveClubs, saveCompetitions, loadBooking, saveBooking


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


def test_date_now():
    date_now = load_datime_now()
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    assert date_now == now


def test_load_clubs():
    listOfClubs = loadClubs()
    assert isinstance(listOfClubs, list)


def test_save_clubs():
    clubs = loadClubs()
    if len(clubs) > 0:
        assert saveClubs(clubs[0]['name'], clubs[0]['points'])


def test_load_competition():
    listOfCompetitions = loadCompetitions()
    assert isinstance(listOfCompetitions, list)


def test_save_competitions():
    competitions = loadCompetitions()
    if len(competitions) > 0:
        assert saveCompetitions(
            competitions[0]['name'], competitions[0]['numberOfPlaces'])


def test_load_booking():
    booking = loadBooking()
    assert isinstance(booking, list)


def test_save_booking():
    competitions = loadCompetitions()
    clubs = loadClubs()
    if len(competitions) > 0 and len(clubs) > 0:
        competition = ""
        club = ""
        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                competition = competition
        for club in clubs:
            if int(club["points"]) > 0:
                club = club
        if isinstance(competition, dict) and isinstance(club, dict):
            pass
