import json
import logging

import pytest

from config.config import URL_SPOTIFY, USER_SPOTIFY
from utils.logger import get_logger
from helpers.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)

class TestUsers:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_users = f"{URL_SPOTIFY}/users"
        cls.rest_client = RestClient()

    @pytest.mark.acceptance
    def test_get_user_profiles(self, log_test_name):
        """
        Test get user profiles
        Get public profile information about a Spotify user.
        """
        url_user_profile = f"{URL_SPOTIFY}/users/{USER_SPOTIFY}"
        response = self.rest_client.request("get", url=url_user_profile)
        LOGGER.info("The user profile: %s", response["body"])

        assert response["status_code"] == 200, "Wrong status code, expected 200"

    @pytest.mark.acceptance
    def test_follow_playlist(self, create_playlist, log_test_name):
        """
        Test follow playlist
        Add the current user as a follower of a playlist.
        """
        body_follow_playlist = {
            "public": False
        }
        id_playlist_created = create_playlist["body"]["id"]
        url_follow_playlist = f"{URL_SPOTIFY}/playlists/{id_playlist_created}/followers"
        response = self.rest_client.request("put", url=url_follow_playlist, body=json.dumps(body_follow_playlist))
        LOGGER.info("The follow playlist: %s", response["body"])

        assert response["status_code"] == 200, "Wrong status code, expected 200"

    @pytest.mark.acceptance
    def test_unfollow_playlist(self, create_playlist, log_test_name):
        """
        Test unfollow playlist
        Remove the current user as a follower of a playlist.
        """
        id_playlist_created = create_playlist["body"]["id"]
        url_unfollow_playlist = f"{URL_SPOTIFY}/playlists/{id_playlist_created}/followers"
        response = self.rest_client.request("delete", url=url_unfollow_playlist)
        LOGGER.info("The unfollow playlist: %s", response["body"])

        assert response["status_code"] == 200, "Wrong status code, expected 200"