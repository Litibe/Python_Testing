import json
import time
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
    competitions_valid = []
    for competition in competitions:
        if competition['date'] > date_now:
            competitions_valid.append(competition)
    if len(competitions_valid) > 0:
        return competitions_valid[randint(0, len(competitions_valid)-1)]
    else:
        return ""


class ServerPerfTest(HttpUser):
    @task()
    def home(self):
        self.client.get("/")

    @task()
    def login(self):
        clubs = load_clubs()
        params = {"email": list_clubs[randint(
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
