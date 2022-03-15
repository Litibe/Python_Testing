from server import load_datime_now
from server import create_app, loadClubs, loadCompetitions, loadBooking
import server as server_file
import json
import pytest
listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()
listOfbooking = loadBooking()


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
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic",
        "date": "2022-10-22 13:30:00",
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
    monkeypatch.setattr(server_file, 'loadCompetitions', mockreturncompt)
    monkeypatch.setattr(server_file, 'loadClubs', mockreturnclubs)
    monkeypatch.setattr(server_file, 'loadBooking', mockreturnbooking)

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


def erase_test_into_json_file():
    with open('clubs.json', "w") as file:
        json.dump({'clubs': listOfClubs}, file, indent=4)
    with open('competitions.json', "w") as file:
        json.dump({'competitions': listOfCompetitions},
                  file, indent=4)
    with open('booking.json', "w") as file:
        json.dump({'booking': listOfbooking}, file, indent=4)


def test_render_context_showSummary_clubs_details_if_compt_valid(client,
                                                                 monkeypatch):
    """
    TEST METHOD
    access booking_page for valid competition
    """
    def mockreturnclubs():
        data = [
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
        return data

    def mockreturncompt():
        data = [
            {
                "name": "Spring Festival",
                        "date": "2020-03-27 10:00:00",
                        "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                        "date": "2022-10-22 13:30:00",
                        "numberOfPlaces": "13"
            }
        ]
        return data

    def mockreturnbooking():
        data = [
        ]
        return data
    monkeypatch.setattr(server_file, 'loadCompetitions', mockreturncompt)
    monkeypatch.setattr(server_file, 'loadClubs', mockreturnclubs)
    monkeypatch.setattr(server_file, 'loadBooking', mockreturnbooking)
    competitions = server_file.loadCompetitions()
    clubs = server_file.loadClubs()
    club = clubs[0]
    club_name = club["name"].split(" ")
    date_now = load_datime_now()
    for competition in competitions:
        print(competition)
        if competition['date'] > date_now:
            competition_valid = competition
            competition_name = competition_valid["name"].split(" ")
            url = "/book/" + competition_name[0] + \
                "%20"+competition_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            response = client.get(url)
            erase_test_into_json_file()
            assert response.status_code == 200
            assert ("How many places?"
                    ).encode() in response.data


def test_post_method_to_book_if_compt_valid(client, monkeypatch):
    """
    TEST METHOD
    try to book with one place with comptetition valid
    """
    def mockreturnclubs():
        data = data_clubs
        return data

    def mockreturncompt():
        data = data_competitions
        return data

    def mockreturnbooking():
        data = data_booking
        return data
    monkeypatch.setattr(server_file, 'loadCompetitions', mockreturncompt)
    monkeypatch.setattr(server_file, 'loadClubs', mockreturnclubs)
    monkeypatch.setattr(server_file, 'loadBooking', mockreturnbooking)
    competitions = server_file.loadCompetitions()
    clubs = server_file.loadClubs()

    for club in clubs:
        if int(club["points"]) > 0:
            club_with_places = club
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0:

            competition_valid = competition
            print(competition)
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_valid['name']
            # try to book with one place but comptetition is finished
            data['places'] = 1
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Great-booking complete!").encode() in response.data
    erase_test_into_json_file()


def test_post_method_to_TWO_book_if_compt_valid(client, monkeypatch):
    """
    TEST METHOD
    try to book with one place with comptetition valid X2
    """
    def mockreturnclubs():
        data = data_clubs
        return data

    def mockreturncompt():
        data = data_competitions
        return data

    def mockreturnbooking():
        data = data_booking
        return data
    monkeypatch.setattr(server_file, 'loadCompetitions', mockreturncompt)
    monkeypatch.setattr(server_file, 'loadClubs', mockreturnclubs)
    monkeypatch.setattr(server_file, 'loadBooking', mockreturnbooking)
    competitions = server_file.loadCompetitions()
    clubs = server_file.loadClubs()
    club_with_places = []
    for club in clubs:
        if int(club["points"]) > 0:
            club_with_places.append(club)
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0 and len(club_with_places) > 1:
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
    erase_test_into_json_file()
