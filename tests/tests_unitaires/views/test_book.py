import email
import pytest
from server import create_app, loadClubs, loadCompetitions, load_datime_now

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


def test_render_context_showSummary_clubs_details_if_compt_valid(client):
    """
    TEST METHOD
    access booking_page for valid competition
    """
    club = clubs[0]
    club_name = club["name"].split(" ")
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] > date_now:
            competition_valid = competition
            competition_name = competition_valid["name"].split(" ")
            url = "/book/" + competition_name[0] + \
                "%20"+competition_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            response = client.get(url)
            assert response.status_code == 200
            assert ("Places available: " +
                    competition_valid['numberOfPlaces']
                    ).encode() in response.data


def test_render_context_showSummary_clubs_details_if_compt_invalid(client):
    """
    TEST METHOD
    comptetition is finished don't access booking_page
    """
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


def test_post_method_to_book_if_compt_invalid(client):
    """
    TEST METHOD
    try to book with one place but comptetition is finished
    """
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


def test_post_method_to_book_if_compt_valid(client):
    """
    TEST METHOD
    try to book with one place with comptetition valid
    """
    for club in clubs:
        if int(club["points"]) > 0:
            club_with_places = club
    date_now = load_datime_now()
    for competition in competitions:
        if competition['date'] > date_now and int(
                competition["numberOfPlaces"]) > 0:
            competition_valid = competition
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_valid['name']
            # try to book with one place but comptetition is finished
            data['places'] = 0
            url = "/purchasePlaces"
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert (
                "Great-booking complete!").encode() in response.data
