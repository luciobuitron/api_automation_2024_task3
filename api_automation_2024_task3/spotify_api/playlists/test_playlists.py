import json
import logging
import pytest

from config.config import URL_SPOTIFY, USER_SPOTIFY
from utils.logger import get_logger
from helpers.rest_client import RestClient
from datetime import datetime
#from config.authentication import authentication

LOGGER = get_logger(__name__, logging.DEBUG)

# ts stores the time in order to have a Playlist name distinguisable
current_datetime = datetime.now()
ts = current_datetime.strftime("%H:%M:%S, %b %d %Y")

class TestPlaylists:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_playlists = f"{URL_SPOTIFY}/playlists"
        cls.list_playlists = []
        cls.rest_client = RestClient()

    @pytest.mark.acceptance
    def test_get_user_playlists(self, log_test_name):
        """
        Test get user playlists
        Get a playlist owned by a Spotify user.
        """

        # Generating a new code value for authentication/authorization
        # from config.authentication import spotify_authentication
        # with authentication.test_request_context('/login'):
        #     authentication.preprocess_request()
        #     spotify_authentication()

        url_user_playlist = f"{URL_SPOTIFY}/users/{USER_SPOTIFY}/playlists"
        response = self.rest_client.request("get", url=url_user_playlist)

        assert response["status_code"] == 200, "Wrong status code, expected 200"

    @pytest.mark.acceptance
    def test_create_playlist(self, log_test_name):
        """
        Test create playlist
        Create a playlist for a Spotify user. (The playlist will be empty until you add tracks.) Each user is generally limited to a maximum of 11000 playlists.
        """
        body_playlist = {
            "name": f"New Playlist #{ts} (No Fixture)",
            "description": f"New playlist description #{ts} (No Fixture)"
        }
        url_create_playlist = f"{URL_SPOTIFY}/users/{USER_SPOTIFY}/playlists"
        response = self.rest_client.request("post", url=url_create_playlist, body=json.dumps(body_playlist))

        assert response["status_code"] == 201, "Wrong status code, expected 201"

    @pytest.mark.functional
    def test_create_playlist_duplicated(self, get_playlist, log_test_name):
        """
        Test create playlist with duplicate name
        """
        body_playlist_duplicated = {
            "name": f"{get_playlist}",
            "description": f"New playlist for duplicate scenario."
        }
        url_create_playlist = f"{URL_SPOTIFY}/users/{USER_SPOTIFY}/playlists"
        response = self.rest_client.request("post", url=url_create_playlist, body=json.dumps(body_playlist_duplicated))
        LOGGER.info("The duplicate name is: %s", get_playlist)
        assert response["status_code"] == 201, "Wrong status code, expected 201"

    @pytest.mark.acceptance
    def test_add_item_playlist(self, create_playlist, log_test_name):
        """
        Test add an item to playlist
        Add one or more items to a user's playlist.
        """
        id_playlist_created = create_playlist["body"]["id"]
        url_add_item_playlist = f"{self.url_playlists}/{id_playlist_created}/tracks"
        body_item_playlist = {
            "uris": [
                "spotify:track:57bgtoPSgt236HzfBOd8kj", "spotify:track:2RsAajgo0g7bMCHxwH3Sk0"
            ],
            "position": 0
        }
        response = self.rest_client.request("post", url=url_add_item_playlist, body=json.dumps(body_item_playlist))

        assert response["status_code"] == 200, "Wrong status code, expected 200"

    @pytest.mark.acceptance
    def test_remove_item_playlist(self, create_playlist, log_test_name):
        """
        Test remove an item from playlist
        Remove one or more items from a user's playlist.
        """
        id_playlist_created = create_playlist["body"]["id"]
        id_snapshot_playlist_created = create_playlist["body"]["snapshot_id"]
        url_remove_item_playlist = f"{self.url_playlists}/{id_playlist_created}/tracks"
        body_item_playlist = {
            "tracks": [
                { "uri": "spotify:track:57bgtoPSgt236HzfBOd8kj" },
                { "uri": "spotify:track:2RsAajgo0g7bMCHxwH3Sk0" }
            ]
        }

        response = self.rest_client.request("delete", url=url_remove_item_playlist, body=json.dumps(body_item_playlist))

        assert response["status_code"] == 200, "Wrong status code, expected 200"

    #According Spotify:
    # https://developer.spotify.com/documentation/web-api/concepts/playlists
    # We have no endpoint for deleting a playlist in the Web API; the notion of deleting a playlist is not relevant within the Spotify’s playlist system.
    # Even if you are the playlist’s owner and you choose to manually remove it from your own list of playlists, you are simply unfollowing it.
    # Although this behavior may sound strange, it means that other users who are already following the playlist can keep enjoying it.
    # Manually restoring a deleted playlist through the Spotify Accounts Service is the same thing as following one of your own playlists that you have previously unfollowed.