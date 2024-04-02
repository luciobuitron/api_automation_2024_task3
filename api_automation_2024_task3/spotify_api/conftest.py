import json
import logging

import pytest
import requests
import time

from datetime import datetime
from config.config import URL_SPOTIFY, USER_SPOTIFY, CLIENT_ID_SPOTIFY, SCOPE_SPOTIFY, REDIRECT_URI
from utils.logger import get_logger
from helpers.rest_client import RestClient
from urllib.request import urlopen
from splinter import browser

LOGGER = get_logger(__name__, logging.DEBUG)

# ts stores the time in order to have a Playlist name distinguisable
current_datetime = datetime.now()
ts = current_datetime.strftime("%H:%M:%S, %b %d %Y")

@pytest.fixture()
def create_playlist(request):

    LOGGER.debug("Create playlist From Fixture")
    body_playlist = {
        "name": f"New Playlist #{ts} (From Fixture)",
        "description": f"New Playlist description #{ts} (From Fixture)",
        "public": True
    }
    url_playlist = URL_SPOTIFY+"/users/"+USER_SPOTIFY+"/playlists"
    rest_client = RestClient()
    response = rest_client.request("post", url_playlist, body=json.dumps(body_playlist))

    return response

@pytest.fixture()
def get_playlist():
    rest_client = RestClient()
    response = rest_client.request("get", URL_SPOTIFY+"/users/"+USER_SPOTIFY+"/playlists")
    playlist_name = response["body"]["items"][1]["name"]
    LOGGER.info("Playlist name: %s", playlist_name)

    return playlist_name


@pytest.fixture()
def log_test_name(request):
    LOGGER.info("---------- TEST '%s' STARTED.---------- ", request.node.name)
    def fin():
        LOGGER.info("----------  TEST'%s' COMPLETED.---------- ", request.node.name)

    request.addfinalizer(fin)