import json
import pytest

from server import create_app, loadClubs, loadCompetitions, loadBooking
from server import load_datime_now
import server as server_file

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
        "date": "2020-10-22 13:30:00",
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


def test_render_context_showSummary_clubs_details_if_compt_finished(
        client,
        monkeypatch):
    """
    TEST METHOD
    comptetition is finished don't access booking_page
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
    club = clubs[0]
    club_name = club["name"].split(" ")
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] < date_now:
            competition_invalid = competition
            print(competition)
            competition_name = competition_invalid["name"].split(" ")
            url = "/book/" + competition_name[0] + \
                "%20"+competition_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            response = client.get(url)
            assert response.status_code == 200
            assert (
                "Please Login"
            ).encode() in response.data
            print("Please Login and link book competiton not valid or finished")
    erase_test_into_json_file()


def test_post_method_to_book_if_compt_invalid(client, monkeypatch):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
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
        if competition['date'] < date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_invalid = competition
            print(competition)
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_invalid['name']
            # try to book with one place but comptetition is finished
            data['places'] = 0
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Competition is finished - See the Date !"
            ).encode() in response.data
            print("Competition is finished - See the Date !")
    erase_test_into_json_file()
