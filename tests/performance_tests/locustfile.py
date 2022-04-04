import json
from random import randint
from locust import HttpUser, task
from server import load_clubs, load_compt, load_booking, load_datime_now
import CONSTANTS

list_clubs = load_clubs()
list_compt = load_compt()
list_booking = load_booking()


def search_club_available():
    clubs = load_clubs()
    for club in clubs:
        if int(club["points"]) >= CONSTANTS.POINTS_PER_PLACE:
            return club
    return ""


def search_competiton_available():
    competitions = load_compt()
    date_now = load_datime_now()
    compt_valid = [c for c in competitions if c["date"] > date_now]
    if len(compt_valid) > 0:
        random_number = randint(0, len(compt_valid)-1)
        return compt_valid[random_number]
    else:
        return ""


def on_start_before_launch_flask_server():
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
                "date": "2023-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2022-10-22 13:30:00",
                "numberOfPlaces": "13"
            }
        ]
    data_booking = []
    with open('clubs.json', "w") as file:
        json.dump({'clubs': data_clubs}, file, indent=4)
    with open('competitions.json', "w") as file:
        json.dump({'competitions': data_competitions}, file, indent=4)
    with open('booking.json', "w") as file:
        json.dump({'booking': data_booking}, file, indent=4)


on_start_before_launch_flask_server()


class ServerPerfTest(HttpUser):

    @task()
    def home(self):
        self.client.get("/")

    @task()
    def login(self):
        clubs = load_clubs()
        params = {"email": clubs[randint(
            0, len(clubs)-1)]["email"]}
        self.client.post('/showSummary', data=params)

    @task()
    def show_booking_page(self):
        competition_valid = search_competiton_available()
        clubs = load_clubs()
        club_name = clubs[randint(0, len(clubs)-1)]["name"].split(" ")
        if competition_valid != "":
            compt_name = competition_valid["name"].split(" ")
            url = "/book/" + compt_name[0] + \
                "%20"+compt_name[1] + "/"
            url += club_name[0]+"%20"+club_name[1]
            self.client.get(url)

    @task()
    def booking_places(self):
        club_with_places = search_club_available()
        competition_valid = search_competiton_available()
        if competition_valid != "" and club_with_places != "":
            data = {}
            data["club"] = club_with_places["name"]
            data["competition"] = competition_valid['name']
            data['places'] = 1
            url = "/purchasePlaces"
            self.client.post(url, data=data)

    @task()
    def logout(self):
        self.client.get('/logout')

    def on_stop(self):
        with open('clubs.json', "w") as file:
            json.dump({'clubs': list_clubs}, file, indent=4)
        with open('competitions.json', "w") as file:
            json.dump({'competitions': list_compt}, file, indent=4)
        with open('booking.json', "w") as file:
            json.dump({'booking': list_booking}, file, indent=4)
