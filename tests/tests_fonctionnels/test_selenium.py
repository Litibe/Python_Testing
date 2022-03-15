from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import multiprocessing
import time
import json

from flask_testing import LiveServerTestCase
from selenium import webdriver
import urllib3
from server import create_app, loadClubs, loadCompetitions, loadBooking

multiprocessing.set_start_method("fork")


class TestUserLogin(LiveServerTestCase):
    def create_app(self):
        app = create_app()
        app.config.update(
            LIVESERVER_PORT=8943,
            DEBUG=True,
            TESTING=True,
            LIVESERVER_TIMEOUT=10,
        )
        return app

    def setUp(self):
        """Setup the test driver with Google Chrome"""
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(self.get_server_url())
        self.listOfClubs = loadClubs()
        self.listOfCompetitions = loadCompetitions()
        self.listOfBooking = loadBooking()

    def tearDown(self):
        self.driver.quit()

    def test_server_login(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.get_server_url())
        time.sleep(1)
        self.assertEqual(r.status, 200)
        assert b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in r.data
        assert "Dashbord Points per Clubs :".encode() in r.data
        r = http.request('GET', self.get_server_url())
        time.sleep(1)
        self.assertEqual(r.status, 200)
        assert b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in r.data
        assert "Dashbord Points per Clubs :".encode() in r.data

        # Click login with email
        clubs = loadClubs()
        if len(clubs) > 0:
            all_emails = [club["email"] for club in clubs]
            self.driver.find_element(
                By.NAME, "email").send_keys(all_emails[0])
            self.driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)


class TestBookingWithValidCompetition(LiveServerTestCase):
    def create_app(self):
        self.listOfClubs = loadClubs()
        self.listOfCompetitions = loadCompetitions()
        with open('competitions.json', "w") as file:
            json.dump({
                "competitions": [
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
            },
                file, indent=4)
        self.listOfBooking = loadBooking()

        app = create_app()
        app.config.update(
            LIVESERVER_PORT=8943,
            DEBUG=True,
            TESTING=True,
            LIVESERVER_TIMEOUT=10,
        )
        return app

    def setUp(self):
        """Setup the test driver with Google Chrome"""
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        with open('clubs.json', "w") as file:
            json.dump({'clubs': self.listOfClubs}, file, indent=4)
        with open('competitions.json', "w") as file:
            json.dump({'competitions': self.listOfCompetitions},
                      file, indent=4)
        with open('booking.json', "w") as file:
            json.dump({'booking': self.listOfBooking}, file, indent=4)
        self.driver.quit()

    def test_server_login_and_booking(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.get_server_url())
        self.assertEqual(r.status, 200)
        assert b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in r.data
        assert "Dashbord Points per Clubs :".encode() in r.data
        time.sleep(3)
        # Click login with email
        clubs = loadClubs()
        if len(clubs) > 0:
            all_emails = [club["email"] for club in clubs]
            self.driver.find_element(
                By.NAME, "email").send_keys(all_emails[0])
            self.driver.find_element(By.TAG_NAME, "button").click()
            # seacrh book place
            self.driver.find_element(By.PARTIAL_LINK_TEXT, ("Book")).click()
            time.sleep(3)
            self.driver.find_element(
                By.NAME, "places").send_keys(1)
            self.driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(3)
