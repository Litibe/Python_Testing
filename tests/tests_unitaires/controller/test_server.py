import datetime
import pytest
from server import create_app, load_datime_now, loadClubs, loadCompetitions, places_already_booking, saveClubs, saveCompetitions, loadBooking, saveBooking


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


competitions = loadCompetitions()
clubs = loadClubs()
date_now = load_datime_now()
booking = loadBooking()


def test_date_now():
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    assert date_now == now


def test_load_clubs():
    listOfClubs = loadClubs()
    assert isinstance(listOfClubs, list)


def test_save_clubs():
    if len(clubs) > 0:
        assert saveClubs(clubs[0]['name'], clubs[0]['points'])


def test_load_competition():
    listOfCompetitions = loadCompetitions()
    assert isinstance(listOfCompetitions, list)


def test_save_competitions():
    if len(competitions) > 0:
        assert saveCompetitions(
            competitions[0]['name'], competitions[0]['numberOfPlaces'])


def test_load_booking():
    assert isinstance(booking, list)


def test_save_booking():
    if len(competitions) > 0 and len(clubs) > 0:
        competition = ""
        club = ""
        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                competition = competition
        for club in clubs:
            if int(club["points"]) > 0:
                club = club
        assert isinstance(competition, dict) and isinstance(club, dict)


def test_places_already_booking():
    if len(competitions) > 0 and len(clubs) > 0:
        competition = ""
        club = ""
        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                competition = competition
        for club in clubs:
            if int(club["points"]) > 0:
                club = club

        places = places_already_booking(
            competition["name"], competition["date"], club["name"])
        assert isinstance(places, int)
