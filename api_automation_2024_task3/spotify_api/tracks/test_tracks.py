import logging
import pytest

from config.config import URL_SPOTIFY, LIMIT_TRACKS
from utils.logger import get_logger
from helpers.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)

class TestTracks:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_tracks = f"{URL_SPOTIFY}/tracks"
        cls.url_tracks_me = f"{URL_SPOTIFY}/me/tracks"
        cls.rest_client = RestClient()

    @pytest.mark.acceptance
    def test_get_several_tracks(self, log_test_name):
        """
        Test get several tracks
        Get Spotify catalog information for multiple tracks based on their Spotify IDs.
        """
        track_ids = {"2MLHyLy5z5l5YRp7momlgw,6qUEOWqOzu1rLPUPQ1ECpx"}
        LOGGER.info("The list of tracks ids: %s", track_ids)
        delimiter = ','
        track_ids_plain = delimiter.join(track_ids)
        url_track_ids = f"{self.url_tracks}?ids={track_ids_plain}"
        LOGGER.info("The URL of tracks ids: %s", url_track_ids)

        response = self.rest_client.request("get", url=url_track_ids)
        LOGGER.info("The several tracks: %s", response)

        assert response["status_code"] == 200, "Wrong status code, expected 200"

    @pytest.mark.functional
    def test_get_saved_tracks_limit(self, log_test_name):
        """
        Test get saved tracks
        Get a list of the songs saved in the current Spotify user's 'Your Music' library.
        """
        url_saved_tracks = f"{self.url_tracks_me}?limit={LIMIT_TRACKS}"
        LOGGER.info("The URL of saved tracks over limit allowed: %s", url_saved_tracks)

        response = self.rest_client.request("get", url=url_saved_tracks)
        LOGGER.info("The saved tracks: %s", response)

        assert response["status_code"] == 429, "Wrong status code, expected 429"

    @pytest.mark.acceptance
    def test_save_several_tracks(self, log_test_name):
        """
        Test save several tracks
        Save one or more tracks to the current user's 'Your Music' library.
        """
        save_track_ids = {"1TEZWG1FdjzDdercCguTwj,3z8h0TU7ReDPLIbEnYhWZb"}
        LOGGER.info("The list of tracks ids: %s", save_track_ids)
        delimiter = ','

        save_track_ids_plain = delimiter.join(save_track_ids)
        save_url_track_ids = f"{URL_SPOTIFY}/me/tracks?ids={save_track_ids_plain}"
        LOGGER.info("The URL of save tracks ids: %s", save_url_track_ids)

        response = self.rest_client.request("put", url=save_url_track_ids)

        assert response["status_code"] == 200, "Wrong status code, expected 200"

        # According Spotify, it is required Premium account in order to use API for /v1/me
        # https://community.spotify.com/t5/Spotify-for-Developers/SpotifyApi-403-Forbidden/m-p/5531465#M8580