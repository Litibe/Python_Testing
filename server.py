import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


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
    return True


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def saveCompetitions(competition_name, competition_numberOfPlaces):
    '''
    Save into 'competitions.json', updated places_availables after booking.

            Parameters:
                    competition_name (str): The Competition Nane
                    competition_numberOfPlaces (str): The Competition Places Availables

            Returns:
                    True
    '''
    listOfCompetitions = loadCompetitions()
    for compt in listOfCompetitions:
        if compt["name"] == competition_name:
            compt["numberOfPlaces"] = str(competition_numberOfPlaces)
    with open('competitions.json', "w") as file:
        json.dump({'competitions': listOfCompetitions}, file, indent=4)
    return True


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        if request.form.get('email', '') != '':
            club = [club for club in clubs if club['email']
                    == request.form['email']]
            if club == []:
                return redirect("/")
            else:
                club = club[0]
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [
            c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            max_places = min(
                int(foundCompetition["numberOfPlaces"]), int(foundClub['points']))
            return render_template('booking.html', club=foundClub, competition=foundCompetition, max_places=max_places)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @ app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name']
                       == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        if int(competition['numberOfPlaces']) >= placesRequired:
            competition['numberOfPlaces'] = int(
                competition['numberOfPlaces'])-placesRequired
            club["points"] = str(int(club["points"])-placesRequired)
            return_save_competitions = saveCompetitions(competition["name"],
                                                        (str(competition["numberOfPlaces"])))
            return_save_clubs = saveClubs(
                club_name=club["name"], club_points=str(club["points"]))
            if return_save_competitions and return_save_clubs:
                flash('Great-booking complete!')
            else:
                flash("Something went wrong-please try again")
        max_places = min(
            int(competition["numberOfPlaces"]), int(club['points']))
        return render_template('welcome.html', club=club, competitions=competitions, max_places=max_places)

    # TODO: Add route for points display

    @ app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
