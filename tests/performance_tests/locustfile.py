import json
import time
from random import randint
from locust import HttpUser, between, task
from server import loadClubs, loadCompetitions, loadBooking, load_datime_now

listOfClubs = loadClubs()
listOfCompetitions = loadCompetitions()
listOfbooking = loadBooking()


def erase_test_into_json_file():
    with open('clubs.json', "w") as file:
        json.dump({'clubs': listOfClubs}, file, indent=4)
    with open('competitions.json', "w") as file:
        json.dump({'competitions': listOfCompetitions},
                  file, indent=4)
    with open('booking.json', "w") as file:
        json.dump({'booking': listOfbooking}, file, indent=4)


def search_club_available():
    clubs = loadClubs()
    for club in clubs:
        if int(club["points"]) > 3:
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


def on_start():
    with open('competitions.json', "w") as file:
        json.dump({
            "competitions": [
                {
                    "name": "Spring Festival",
                    "date": "2022-03-27 10:00:00",
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
    with open('clubs.json', "w") as file:
        json.dump({
            "clubs": [
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
        },
            file, indent=4)
    return True


class ServerPerfTest(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def home(self):
        self.client.get("/")

    @task(3)
    def login(self):
        clubs = loadClubs()
        params = {"email": listOfClubs[randint(
            0, len(clubs)-1)]["email"]}
        self.client.post('/showSummary', data=params)

    @task(2)
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

    @task(1)
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

    @task(3)
    def logout(self):
        self.client.get('/logout')
