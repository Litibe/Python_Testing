from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import multiprocessing
import time

from flask_testing import LiveServerTestCase
from selenium import webdriver
import urllib3
from server import create_app

multiprocessing.set_start_method("fork")


class TestUserTakesTheTest(LiveServerTestCase):
    def create_app(self):
        app = create_app()
        app.config.update(
            LIVESERVER_PORT=8943,
            DEBUG=True
        )
        return app

    def setUp(self):
        """Setup the test driver with Google Chrome"""
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.get_server_url())
        time.sleep(1)
        self.assertEqual(r.status, 200)
        assert b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in r.data
