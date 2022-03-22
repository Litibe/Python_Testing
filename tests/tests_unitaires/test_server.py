from server import load_datime_now, load_clubs, load_compt
from server import places_already_booking, save_clubs, save_compt
from server import load_booking
import json
import os

competitions = load_compt()
clubs = load_clubs()
date_now = load_datime_now()
booking = load_booking()


def test_load_clubs():
    list_clubs = load_clubs()
    assert isinstance(list_clubs, list)

    if os.path.exists('clubs.json'):
        os.remove('clubs.json')
        list_clubs = load_clubs()
        assert isinstance(list_clubs, list)
        assert list_clubs == []
        with open('clubs.json', "w") as file:
            json.dump({'clubs': clubs}, file, indent=4)


def test_save_clubs():
    if len(clubs) > 0:
        assert save_clubs(clubs[0]['name'], clubs[0]['points'])


def test_load_competition():
    list_compt = load_compt()
    assert isinstance(list_compt, list)
    if os.path.exists('competitions.json'):
        os.remove('competitions.json')
        list_compt = load_compt()
        assert isinstance(list_compt, list)
        assert list_compt == []
        with open('competitions.json', "w") as file:
            json.dump({'competitions': competitions}, file, indent=4)


def test_save_competitions():
    if len(competitions) > 0:
        assert save_compt(
            competitions[0]['name'], competitions[0]['numberOfPlaces'])


def test_load_booking():
    list_booking = load_booking()
    assert isinstance(list_booking, list)
    if os.path.exists('booking.json'):
        os.remove('booking.json')
        list_booking = load_booking()
        assert isinstance(list_booking, list)
        assert list_booking == []
        with open('booking.json', "w") as file:
            json.dump({'booking': booking}, file, indent=4)


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
