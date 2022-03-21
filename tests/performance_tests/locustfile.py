import json
import time
from random import randint
from locust import HttpUser, task
from server import loadClubs, loadCompetitions, loadBooking, load_datime_now
import CONSTANTS
listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()
listOfbooking = loadBooking()


def search_club_available():
    clubs = loadClubs()
    for club in clubs:
        if int(club["points"]) >= CONSTANTS.POINTS_PER_PLACE:
            return club
    return ""


def search_competiton_available():
    competitions = loadCompetitions()
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
        clubs = loadClubs()
        params = {"email": listOfClubs[randint(
            0, len(clubs)-1)]["email"]}
        self.client.post('/showSummary', data=params)

    @task()
    def show_booking_page(self):
        competition_valid = search_competiton_available()
        clubs = loadClubs()
        club_name = clubs[randint(0, len(clubs)-1)]["name"].split(" ")
        if competition_valid != "":
            competition_name = competition_valid["name"].split(" ")
            url = "/book/" + competition_name[0] + \
                "%20"+competition_name[1] + "/"
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
