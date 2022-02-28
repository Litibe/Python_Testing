from http import server
import datetime
import pytest
from server import create_app, load_datime_now


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_date_now():
    date_now = load_datime_now()
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    assert date_now == now
