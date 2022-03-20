import datetime
import json
import logging
import os
from flask import Flask, render_template, request, redirect, flash, url_for

from CONSTANTS import MAX_BOOKING_PLACES, POINTS_PER_PLACE

logging.basicConfig(level=logging.DEBUG,
                    filename=f"debug_app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')


def loadClubs():
    if os.path.exists('clubs.json'):
        with open('clubs.json') as c:
            data = json.load(c)
            if data.get('clubs', "") != "":
                listOfClubs = data['clubs']
                logging.debug("Load clubs.json and return listOfClubs")
                return listOfClubs
    with open('clubs.json', "w") as file:
        json.dump({'clubs': []}, file, indent=4)
        logging.debug("Init File clubs.json")
        return []


def saveClubs(club_name, club_points):
    '''
    Save into 'clubs.json', updated club_points after booking.

            Parameters:
                    club_name (str): The Club Nane
                    club_points (str): Club's points

            Returns:
                    True
    '''
    listOfClubs = loadClubs()
    for club in listOfClubs:
        if club["name"] == club_name:
            club["points"] = str(club_points)
    with open('clubs.json', "w") as file:
        json.dump({'clubs': listOfClubs}, file, indent=4)
        logging.debug("Save clubs.json")
        return True


def loadCompetitions():
    if os.path.exists('competitions.json'):
        with open('competitions.json') as comps:
            data = json.load(comps)
            if data.get('competitions', "") != "":
                listOfCompetitions = data['competitions']
                logging.debug(
                    " load competitions.json and return competitions")
                return listOfCompetitions
    with open('competitions.json', "w") as file:
        json.dump({'competitions': []}, file, indent=4)
        logging.debug("Init File competitions.json")
        return []


def saveCompetitions(competition_name, competition_numberOfPlaces):
    '''
    Save into 'competitions.json', updated places_availables after booking.

            Parameters:
                    competition_name (str): The Competition Nane
                    competition_numberOfPlaces (str): 
                        The Competition Places Availables

            Returns:
                    True
    '''
    listOfCompetitions = loadCompetitions()
    for compt in listOfCompetitions:
        if compt["name"] == competition_name:
            compt["numberOfPlaces"] = str(competition_numberOfPlaces)
    with open('competitions.json', "w") as file:
        json.dump({'competitions': listOfCompetitions}, file, indent=4)
        logging.debug("saveCompetitions OK")
        return True


def load_datime_now():
    '''
    Create date now
            Returns:
                    date now - format : "%Y-%m-%d %H:%M:%S"
    '''
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.debug("load_datime_now OK")
    return now


def loadBooking():
    '''
    Load 'booking.json' and if not exist create it.

        Returns:
            listOfBooking
    '''
    if os.path.exists("booking.json"):
        with open('booking.json') as file:
            listOfBooking = json.load(file)['booking']
            logging.debug("loadBooking ok")
            return listOfBooking
    else:
        with open('booking.json', "w") as file:
            json.dump({'booking': []}, file, indent=4)
            logging.debug("INIT booking.json  ok")
            return []


def saveBooking(competition_name, competition_date, club_name, placesRequired):
    '''
    Save into 'booking.json', update booking for competition_name,
     club_name with club_places.

            Parameters:
                    competition_name (str): The Competition Nane
                    competition_date (format date -
                        format : "%Y-%m-%d %H:%M:%S")
                    club_name (str) : The Club Name
                    placesRequired (int) :
                        The number of booking places for competition

            Returns:
                    listOfBooking
    '''
    listOfBooking = loadBooking()
    if len(listOfBooking) > 0:
        i = 0
        for events in listOfBooking:
            for event_date, event_values in events.items():
                if event_date == competition_date:
                    logging.debug(
                        "saveBooking : detect EVENT_DATE already into file")
                    # search if competitio_name already into file
                    if event_values.get(competition_name, "") != "":
                        if event_values.get(competition_name, "").get(club_name,
                                                                      "") != "":
                            event_values[competition_name][club_name] = str(
                                int(event_values[competition_name][club_name]) + int(
                                    placesRequired))
                            i += 1
                            logging.debug(
                                "saveBooking : for EVENT_DATE detect COMPETITON and CLUB UPDATE placesRequired")
                        else:
                            i += 1
                            event_values[competition_name][club_name] = str(
                                placesRequired)
                            logging.debug(
                                "saveBooking : for EVENT_DATE detect COMPETITON and add CLUB  placesRequired")
                    else:
                        logging.debug(
                            "saveBooking : for EVENT_DATE Create COMPETITON and add CLUB with places")
                        event_values[competition_name] = {
                            club_name: str(placesRequired)
                        }
                        i += 1

        if i == 0:
            logging.debug("saveBooking : create new EVENT_DATE")
            data = {competition_date: {
                competition_name: {
                    club_name: str(placesRequired)
                }
            }}
            listOfBooking.append(data)
    else:
        logging.debug("saveBooking : len(listOfBooking) NULL")
        data = {competition_date: {
            competition_name: {
                club_name: str(placesRequired)
            }
        }}
        listOfBooking.append(data)
    with open('booking.json', "w") as file:
        json.dump({'booking': listOfBooking}, file, indent=4)
        logging.debug("saveBooking into booking.json")
        return listOfBooking


def places_already_booking(competition_name, competition_date, club_name):
    '''
        load 'booking.json' and search booking_places
        for date/competition_name/club_name.

                Parameters:
                        competition_name (str): The Competition Nane
                        competition_date (format date 
                        - format : "%Y-%m-%d %H:%M:%S") 
                        club_name (str) : The Club Name
                Returns:
                        places (int)
    '''
    listOfBooking = loadBooking()
    places = 0
    if len(listOfBooking) > 0:
        for events in listOfBooking:
            for event_date, event_values in events.items():
                if event_date == competition_date:
                    # search if competitio_name already into file
                    if event_values.get(competition_name, "") != "":
                        if event_values.get(competition_name, ""
                                            ).get(club_name, "") != "":
                            places = int(
                                event_values[competition_name][club_name])
    return places


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html', clubs=clubs)

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        if request.form.get('email', '') != '':
            club = [club for club in clubs if club['email']
                    == request.form['email']]
            if club == []:
                logging.warning(
                    "GET /showSummary : club not found into json")
                return redirect("/")
            else:
                club = club[0]
            date_now = load_datime_now()
            booking = loadBooking()
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions,
                                   date_now=date_now, booking=booking,
                                   max_booking_places=MAX_BOOKING_PLACES,
                                   points_per_place=POINTS_PER_PLACE)
        else:
            return redirect("/")

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club]
        if foundClub == []:
            logging.warning(
                "GET /book/<competition>/<club> : club not found into json")
            return redirect("/")
        else:
            foundClub = foundClub[0]
        foundCompetition = [
            c for c in competitions if c['name'] == competition]
        if foundCompetition == []:
            logging.warning(
                "GET /book/<competition>/<club> : compt not found into json")
            return redirect("/")
        else:
            foundCompetition = foundCompetition[0]
        date_now = load_datime_now()
        booking = loadBooking()
        already_places = places_already_booking(
            foundCompetition["name"],
            foundCompetition["date"],
            foundClub["name"])
        if foundClub and foundCompetition and (
                date_now < foundCompetition['date']):
            max_places_comp = min(
                int(
                    foundCompetition["numberOfPlaces"]), (int(
                        foundClub['points'])//POINTS_PER_PLACE))
            max_places_club = int(
                foundClub['points'])//POINTS_PER_PLACE
            max_places = min(
                max_places_comp, MAX_BOOKING_PLACES, max_places_club,
                MAX_BOOKING_PLACES-already_places)
            if max_places < 0:
                max_places = 0
            logging.debug("GET /book/<competition>/<club> : OK")
            return render_template('booking.html',
                                   club=foundClub,
                                   competition=foundCompetition,
                                   max_places=max_places,
                                   already_places=already_places,
                                   max_booking_places=MAX_BOOKING_PLACES,
                                   points_per_place=POINTS_PER_PLACE)
        else:
            flash("Something went wrong-please try again")
            logging.error(
                "GET /book/<competition>/<club> :pb found club/compt or date_now > date_compt")
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions,
                                   date_now=date_now,
                                   booking=booking,
                                   max_booking_places=MAX_BOOKING_PLACES,
                                   points_per_place=POINTS_PER_PLACE)

    @ app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        date_now = load_datime_now()
        competition = [c for c in competitions if c['name']
                       == request.form['competition']]
        if competition == []:
            flash(
                "Something went wrong-please try again")
            logging.error(
                "POST /purchasePlaces : competition_name not in json_file")
            competition = ""
        else:
            competition = competition[0]
        club = [c for c in clubs if c['name'] == request.form['club']]
        if club == []:
            flash(
                "Something went wrong-please try again")
            logging.error("POST /purchasePlaces : club_name not in json_file")
            club = ""
        else:
            club = club[0]
        placesRequired = int(request.form['places'])

        if date_now > competition['date']:
            flash("Competition is finished - See the Date !")
            logging.error("POST /purchasePlaces : Competition is finished")
        if competition != "" and club != "" and placesRequired > 0 and date_now < competition['date']:
            if int(competition['numberOfPlaces']) >= placesRequired:
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces'])-placesRequired
                club["points"] = int(club["points"]) - \
                    int(POINTS_PER_PLACE)*int(placesRequired)
                save_competitions = saveCompetitions(
                    competition["name"],
                    (str(competition["numberOfPlaces"])))
                save_clubs = saveClubs(
                    club_name=club["name"],
                    club_points=str(club["points"]))
                booking = saveBooking(
                    competition["name"],
                    competition["date"],
                    club["name"],
                    placesRequired
                )
                if save_competitions and save_clubs:
                    flash('Great-booking complete!')
                    logging.debug(
                        "POST / purchasePlaces: Great-booking complete!")
                else:
                    flash(
                        "Something went wrong-please try again")
                    logging.error("POST / purchasePlaces: save error")
            else:
                booking = loadBooking()
                flash(
                    "Number of places requested greater than the number of places authorized for you")
                logging.error(
                    "POST / purchasePlaces: Number of places requested greater than the number of places authorized for you")

        else:
            booking = loadBooking()
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               date_now=date_now,
                               booking=booking,
                               max_booking_places=MAX_BOOKING_PLACES,
                               points_per_place=POINTS_PER_PLACE)

    @ app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
