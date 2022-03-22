from server import create_app, load_clubs, load_compt, load_booking
import server as server_file
import pytest
list_clubs = load_clubs()
list_compt = load_compt()
list_booking = load_booking()


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


def test_request_index(client):
    response = client.get("/")
    elementhtml = "<h1>Welcome to the GUDLFT Registration Portal!</h1>"
    assert elementhtml.encode() in response.data
    elementhtml = data_clubs[0]['name']
    assert elementhtml.encode() in response.data
    elementhtml = data_clubs[1]['name']
    assert elementhtml.encode() in response.data
    elementhtml = data_clubs[2]['name']
    assert elementhtml.encode() in response.data
    assert response.status_code == 200


def test_request_correct_login(client):
    params = {"email": data_clubs[0]["email"]}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 200


def test_request_incorrect_login(client):
    params = {"email": "test@test.fr"}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 302


def test_request_incorrect_login_form(client):
    params = {"email": ""}
    response = client.post('/showSummary', data=params)
    assert response.status_code == 302


def test_request_correct_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_render_context_showSummary_clubs_details(client):
    clubs = server_file.load_clubs()
    response = client.post(
        "/showSummary", data={"email":  clubs[0]['email']})
    assert response.status_code == 200
    assert ("Points available: "+clubs[0]['points']).encode() in response.data
    assert clubs[0]['email'].encode() in response.data


def test_booking_page_valid_compt_club(client):
    competitions = server_file.load_compt()
    clubs = server_file.load_clubs()
    compt_name = competitions[1]["name"].split(" ")
    club_name = clubs[0]["name"].split(" ")
    url = "/book/" + compt_name[0] + \
        "%20"+compt_name[1] + "/"
    url += club_name[0]+"%20"+club_name[1]
    response = client.get(url)

    assert response.status_code == 200
    assert competitions[1]["name"].encode() in response.data
    test_input_club = '<input type="hidden" name="club" value="' + \
        clubs[0]["name"]+'" />'
    assert test_input_club.encode() in response.data
    assert (clubs[0]['points'] + " points").encode() in response.data


def test_booking_page_valid_club_invalid_compt(client):
    competitions = {"name": 'Miami Week'}
    clubs = server_file.load_clubs()
    compt_name = competitions["name"].split(" ")
    club_name = clubs[0]["name"].split(" ")
    url = "/book/" + compt_name[0] + \
        "%20"+compt_name[1] + "/"
    url += club_name[0]+"%20"+club_name[1]
    response = client.get(url)
    assert response.status_code == 302


def test_booking_page_invalid_compt_club(client):
    competitions = "MIAMI"
    clubs = "TOTO CLUB"
    club_name = clubs.split(" ")
    url = "/book/" + competitions + "/"
    url += club_name[0]+"%20"+club_name[1]
    response = client.get(url)
    assert response.status_code == 302
