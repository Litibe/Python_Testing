from server import load_datime_now, loadClubs, loadCompetitions
from server import places_already_booking, saveClubs, saveCompetitions
from server import loadBooking
import json
import os

competitions = loadCompetitions()
clubs = loadClubs()
date_now = load_datime_now()
booking = loadBooking()


def test_load_clubs():
    listOfClubs = loadClubs()
    assert isinstance(listOfClubs, list)

    if os.path.exists('../../clubs.json'):
        os.path.remove('../../clubs.json')
        listOfClubs = loadClubs()
        assert isinstance(listOfClubs, list)
        assert listOfClubs == []
        with open('../../clubs.json', "w") as file:
            json.dump({'clubs': clubs}, file, indent=4)


def test_save_clubs():
    if len(clubs) > 0:
        assert saveClubs(clubs[0]['name'], clubs[0]['points'])


def test_load_competition():
    listOfCompetitions = loadCompetitions()
    assert isinstance(listOfCompetitions, list)
    if os.path.exists('../../competitions.json'):
        os.path.remove('../../competitions.json')
        listOfCompetitions = loadCompetitions()
        assert isinstance(listOfCompetitions, list)
        assert listOfCompetitions == []
        with open('../../competitions.json', "w") as file:
            json.dump({'competitions': competitions}, file, indent=4)


def test_save_competitions():
    if len(competitions) > 0:
        assert saveCompetitions(
            competitions[0]['name'], competitions[0]['numberOfPlaces'])


def test_load_booking():
    assert isinstance(booking, list)


def test_save_booking():
    if len(competitions) > 0 and len(clubs) > 0:
        competition = ""
        club = ""
        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                competition = competition
        for club in clubs:
            if int(club["points"]) > 0:
                club = club
        assert isinstance(competition, dict) and isinstance(club, dict)


def test_places_already_booking():
    if len(competitions) > 0 and len(clubs) > 0:
        competition = ""
        club = ""
        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                competition = competition
        for club in clubs:
            if int(club["points"]) > 0:
                club = club

        places = places_already_booking(
            competition["name"], competition["date"], club["name"])
        assert isinstance(places, int)
