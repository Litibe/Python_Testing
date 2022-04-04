import json
from CONSTANTS import POINTS_PER_PLACE
from server import load_datime_now
from server import create_app, load_booking
import server as server_file
import pytest

list_booking = load_booking()
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
        "name": "Spring Festival2023",
        "date": "2023-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic2022",
        "date": "2022-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
]


@pytest.fixture()
def app(monkeypatch):
    def mock_load_clubs():
        data = data_clubs
        return data

    def mock_load_compt():
        data = data_competitions
        return data

    def mock_save_compt(compt_name, compt_places):
        return True

    def mock_save_clubs(club_name, club_points):
        return True

    monkeypatch.setattr(server_file, 'load_compt', mock_load_compt)
    monkeypatch.setattr(server_file, 'save_compt', mock_save_compt)
    monkeypatch.setattr(server_file, 'load_clubs', mock_load_clubs)
    monkeypatch.setattr(server_file, 'save_clubs', mock_save_clubs)

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


def test_render_context_showSummary_clubs_details_if_compt_valid(client):
    """
    TEST METHOD
    access booking_page for valid competition
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    club = clubs[0]
    club_name = club["name"].split(" ")
    for competition in competitions:
        print(competition)
        if competition['date'] > date_now:
            competition_valid = competition
            compt_name = competition_valid["name"].split(" ")
            url = "/book/" + compt_name[0] + \
                "%20"+compt_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            response = client.get(url)
            assert response.status_code == 200
            assert ("How many places?"
                    ).encode() in response.data


def test_post_method_to_book_if_compt_valid(client, monkeypatch):
    """
    TEST METHOD
    try to book with one place with comptetition valid
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    for club in clubs:
        if int(club["points"]) > POINTS_PER_PLACE:
            club_with_places = club
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_valid = competition
            print(competition)
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_valid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Great-booking complete!").encode() in response.data


def test_post_method_to_TWO_book_if_compt_valid(client):
    """
    TEST METHOD
    try to book with one place with comptetition valid X2
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    club_with_places = []
    for club in clubs:
        if int(club["points"]) > POINTS_PER_PLACE:
            club_with_places.append(club)
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0 and len(
                    club_with_places) > 0:
            competition_valid = competition
            print(competition)
            data = {}
            data["club"] = club_with_places[0]["name"]
            data["competition"] = competition_valid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            data["club"] = club_with_places[0]["name"]
            response = client.post(url, data=data)
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Great-booking complete!").encode() in response.data


def test_post_method_to_TWO_book_with_2_compt_valid(client):
    """
    TEST METHOD
    try to book with one place with comptetition valid X2
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    club_with_places = []
    for club in clubs:
        if int(club["points"]) > POINTS_PER_PLACE:
            club_with_places.append(club)
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0 and len(
                    club_with_places) > 0:
            competition_valid = competition
            data = {}
            data["club"] = club_with_places[0]["name"]
            data["competition"] = competition_valid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            data["club"] = club_with_places[0]["name"]
            response = client.post(url, data=data)
            data["club"] = club_with_places[1]["name"]
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Great-booking complete!").encode() in response.data


def test_post_method_to_book_another_places_with_2_compt_valid(client):
    """
    TEST METHOD
    try to book with one place with comptetition valid X2 again
    """
    test_post_method_to_TWO_book_with_2_compt_valid(client)
    booking = load_booking()
    print("booking_list : ", booking)


def test_post_method_to_book_if_compt_valid_but_error_places(
        client):
    """
    TEST METHOD
    try to book with one place with comptetition valid but error places
    """
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    club_with_places = ""
    for club in clubs:
        if int(club["points"]) > POINTS_PER_PLACE:
            club_with_places = club
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0 and club_with_places != "":
            competition_valid = competition
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_valid['name']
            data['places'] = 42
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            msg = "Number of places requested greater"
            assert msg.encode() in response.data
    # erase booking.JSON MODIFY
    with open('booking.json', "w") as file:
        json.dump({'booking': list_booking}, file, indent=4)
