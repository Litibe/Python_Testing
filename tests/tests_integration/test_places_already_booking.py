import json
import pytest
from server import create_app, loadClubs, loadCompetitions, loadBooking
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
data_booking = [
    {
        "2022-10-22 13:30:00": {
            "Fall Classic": {
                "She Lifts": "1",
                "Simply Lift": "1",
                "Iron Temple": "2"
            }
        }
    }
]


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


def test_request_booking(client):
    url = 'book/Fall%20Classic/She%20Lifts'
    response = client.get(url)
    assert response.status_code == 200
    erase_test_into_json_file()
