from server import load_datime_now
from server import create_app, loadClubs, loadCompetitions, loadBooking
import json
import pytest
listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()
listOfbooking = loadBooking()


@pytest.fixture()
def app():
    with open('competitions.json', "w") as file:
        json.dump({
            "competitions": [
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
        },
            file, indent=4)
    with open('booking.json', "w") as file:
        json.dump({
            "booking": [
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
        },
            file, indent=4)
    app = create_app()
    app.config.update({
        "TESTING": True,
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
