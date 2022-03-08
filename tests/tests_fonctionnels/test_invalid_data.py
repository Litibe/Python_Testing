import json
import pytest
from server import create_app, loadClubs, loadCompetitions, loadBooking
from server import load_datime_now
listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()
listOfbooking = loadBooking()


@pytest.fixture()
def app():
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


def test_render_context_showSummary_clubs_details_if_compt_invalid(client):
    """
    TEST METHOD
    comptetition is finished don't access booking_page
    """
    clubs = loadClubs()
    competitions = loadCompetitions()
    club = clubs[0]
    club_name = club["name"].split(" ")
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] < date_now:
            competition_invalid = competition
            competition_name = competition_invalid["name"].split(" ")
            url = "/book/" + competition_name[0] + \
                "%20"+competition_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            response = client.get(url)
            assert response.status_code == 200
            assert (
                "Something went wrong-please try again"
            ).encode() in response.data
    erase_test_into_json_file()


def test_post_method_to_book_if_compt_invalid(client):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
    """
    clubs = loadClubs()
    competitions = loadCompetitions()
    for club in clubs:
        if int(club["points"]) > 0:
            club_with_places = club
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] < date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_invalid = competition
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
    erase_test_into_json_file()
