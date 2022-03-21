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


def load_clubs():
    if os.path.exists('clubs.json'):
        with open('clubs.json') as c:
            data = json.load(c)
            if data.get('clubs', "") != "":
                list_clubs = data['clubs']
                logging.debug("Load clubs.json and return list_clubs")
                return list_clubs
    with open('clubs.json', "w") as file:
        json.dump({'clubs': []}, file, indent=4)
        logging.debug("Init File clubs.json")
        return []


def save_clubs(club_name, club_points):
    '''
    Save into 'clubs.json', updated club_points after booking.

            Parameters:
                    club_name (str): The Club Nane
                    club_points (str): Club's points

            Returns:
                    True
    '''
    list_clubs = load_clubs()
    for club in list_clubs:
        if club["name"] == club_name:
            club["points"] = str(club_points)
    with open('clubs.json', "w") as file:
        json.dump({'clubs': list_clubs}, file, indent=4)
        logging.debug("Save clubs.json")
        return True


def load_compt():
    if os.path.exists('competitions.json'):
        with open('competitions.json') as comps:
            data = json.load(comps)
            if data.get('competitions', "") != "":
                list_compt = data['competitions']
                logging.debug(
                    " load competitions.json and return competitions")
                return list_compt
    with open('competitions.json', "w") as file:
        json.dump({'competitions': []}, file, indent=4)
        logging.debug("Init File competitions.json")
        return []


def save_compt(compt_name, compt_places):
    '''
    Save into 'competitions.json', updated places_availables after booking.

            Parameters:
                    compt_name (str): The Competition Nane
                    compt_places (str):
                        The Competition Places Availables

            Returns:
                    True
    '''
    list_compt = load_compt()
    for compt in list_compt:
        if compt["name"] == compt_name:
            compt["numberOfPlaces"] = str(compt_places)
    with open('competitions.json', "w") as file:
        json.dump({'competitions': list_compt}, file, indent=4)
        logging.debug("save_compt OK")
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


def load_booking():
    '''
    Load 'booking.json' and if not exist create it.

        Returns:
            list_booking
    '''
    if os.path.exists("booking.json"):
        with open('booking.json') as file:
            list_booking = json.load(file)['booking']
            logging.debug("load_booking ok")
            return list_booking
    else:
        with open('booking.json', "w") as file:
            json.dump({'booking': []}, file, indent=4)
            logging.debug("INIT booking.json  ok")
            return []


def save_booking(compt_name, compt_date, club_name, places_buy):
    '''
    Save into 'booking.json', update booking for compt_name,
     club_name with club_places.

            Parameters:
                    compt_name (str): The Competition Nane
                    compt_date (format date -
                        format : "%Y-%m-%d %H:%M:%S")
                    club_name (str) : The Club Name
                    places_buy (int) :
                        The number of booking places for competition

            Returns:
                    list_booking
    '''
    list_booking = load_booking()
    if len(list_booking) > 0:
        i = 0
        for events in list_booking:
            for event_date, event_values in events.items():
                if event_date == compt_date:
                    logging.debug(
                        "save_booking : detect EVENT_DATE already into file")
                    # search if competitio_name already into file
                    if event_values.get(compt_name, "") != "":
                        if event_values.get(compt_name, "").get(club_name,
                                                                "") != "":
                            event_values[compt_name][club_name] = str(
                                int(event_values[compt_name][club_name]) + int(
                                    places_buy))
                            i += 1
                            logging.debug(
                                "save_booking : for EVENT_DATE detect\
                                    COMPETITON and CLUB UPDATE places_buy")
                        else:
                            i += 1
                            event_values[compt_name][club_name] = str(
                                places_buy)
                            logging.debug(
                                "save_booking : for EVENT_DATE detect \
                                    COMPETITON and add CLUB  places_buy")
                    else:
                        logging.debug(
                            "save_booking : for EVENT_DATE Create COMPETITON\
                                 and add CLUB with places")
                        event_values[compt_name] = {
                            club_name: str(places_buy)
                        }
                        i += 1

        if i == 0:
            logging.debug("save_booking : create new EVENT_DATE")
            data = {compt_date: {
                compt_name: {
                    club_name: str(places_buy)
                }
            }}
            list_booking.append(data)
    else:
        logging.debug("save_booking : len(list_booking) NULL")
        data = {compt_date: {
            compt_name: {
                club_name: str(places_buy)
            }
        }}
        list_booking.append(data)
    with open('booking.json', "w") as file:
        json.dump({'booking': list_booking}, file, indent=4)
        logging.debug("save_booking into booking.json")
        return list_booking


def places_already_booking(compt_name, compt_date, club_name):
    '''
        load 'booking.json' and search booking_places
        for date/compt_name/club_name.

                Parameters:
                        compt_name (str): The Competition Nane
                        compt_date (format date
                        - format : "%Y-%m-%d %H:%M:%S")
                        club_name (str) : The Club Name
                Returns:
                        places (int)
    '''
    list_booking = load_booking()
    places = 0
    if len(list_booking) > 0:
        for events in list_booking:
            for event_date, event_values in events.items():
                if event_date == compt_date:
                    # search if competitio_name already into file
                    if event_values.get(compt_name, "") != "":
                        if event_values.get(compt_name, ""
                                            ).get(club_name, "") != "":
                            places = int(
                                event_values[compt_name][club_name])
    return places


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'

    competitions = load_compt()
    clubs = load_clubs()

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
            booking = load_booking()
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
        booking = load_booking()
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
                """GET /book/<competition>/<club> :pb found
                club/compt /or date_now > date_compt""")
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
                "POST /purchasePlaces : compt_name not in json_file")
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
        places_buy = int(request.form['places'])

        if date_now > competition['date']:
            flash("Competition is finished - See the Date !")
            logging.error("POST /purchasePlaces : Competition is finished")
        if competition != "" and club != "" and \
                places_buy > 0 and date_now < competition['date']:
            if int(competition['numberOfPlaces']) >= places_buy:
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces'])-places_buy
                club["points"] = int(club["points"]) - \
                    int(POINTS_PER_PLACE)*int(places_buy)
                save_competitions = save_compt(
                    competition["name"],
                    (str(competition["numberOfPlaces"])))
                save_club = save_clubs(
                    club_name=club["name"],
                    club_points=str(club["points"]))
                booking = save_booking(
                    competition["name"],
                    competition["date"],
                    club["name"],
                    places_buy
                )
                if save_competitions and save_club:
                    flash('Great-booking complete!')
                    logging.debug(
                        "POST / purchasePlaces: Great-booking complete!")
                else:
                    flash(
                        "Something went wrong-please try again")
                    logging.error("POST / purchasePlaces: save error")
            else:
                booking = load_booking()
                flash(
                    "Number of places requested greater than \
                        the number of places authorized for you")
                logging.error(
                    "POST / purchasePlaces: Number of places \
                        requested greater than the number of places \
                            authorized for you")

        else:
            booking = load_booking()
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
