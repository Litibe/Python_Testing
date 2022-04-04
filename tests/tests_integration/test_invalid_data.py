import pytest

from server import create_app
from server import load_datime_now
import server as server_file

date_now = load_datime_now()

data_clubs = [
    {
        "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13"
    },
    {
        "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
    },
    {
        "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
    }
]
data_competitions = [
    {
        "name": "Spring Festival",
        "date": "2019-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic",
        "date": "2019-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
]
data_booking = []


@pytest.fixture()
def app(monkeypatch):
    def mockreturnclubs():
        data = data_clubs
        return data

    def mockreturncompt():
        data = data_competitions
        return data

    def mockreturnbooking():
        data = data_booking
        return data
    monkeypatch.setattr(server_file, 'load_compt', mockreturncompt)
    monkeypatch.setattr(server_file, 'load_clubs', mockreturnclubs)
    monkeypatch.setattr(server_file, 'load_booking', mockreturnbooking)
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": True,
        "LIVESERVER_PORT": 8943,
        "LIVESERVER_TIMEOUT": 10,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_render_context_showSummary_clubs_details_if_compt_finished(
        client):
    """
    TEST METHOD
    comptetition is finished don't access booking_page
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    club = clubs[0]
    club_name = club["name"].split(" ")
    for competition in competitions:
        if competition['date'] < date_now:
            competition_invalid = competition
            print(competition)
            compt_name = competition_invalid["name"].split(" ")
            url = "/book/" + compt_name[0] + \
                "%20"+compt_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            response = client.get(url)
            assert response.status_code == 200
            assert (
                "Please Login"
            ).encode() in response.data
            print("Competition not valid or finished")


def test_post_method_to_book_if_compt_invalid(client):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    for club in clubs:
        if int(club["points"]) > 0:
            club_with_places = club
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] < date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_invalid = competition
            print(competition)
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_invalid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Competition is finished - See the Date !"
            ).encode() in response.data
            print("Competition is finished ! purchasePlaces error")


def test_post_method_to_book_if_compt_none(client):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    for club in clubs:
        if int(club["points"]) > 0:
            club_with_places = club
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] < date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_invalid = competition
            print(competition)
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_invalid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Competition is finished - See the Date !"
            ).encode() in response.data
            print("Competition is finished - See the Date !")


def test_post_method_to_book_if_clubs_none(client):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
    """
    competitions = server_file.load_compt()
    for competition in competitions:
        if competition['date'] < date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_invalid = competition
            data = {}
            data["club"] = "none"
            data["competition"] = competition_invalid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200


def test_post_method_to_book_if_clubs_compt_none(client):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
    """
    data = {}
    data["club"] = "none"
    data["competition"] = "none"
    data['places'] = 1
    url = "/purchasePlaces"
    response = client.post(url, data=data)
    assert response.status_code == 200
