# Package to connect to Spotify API and retrieve data
# This package assumes you have a Spotify API client_id and client_secret
# in your environment variables.
# SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI
# See https://developer.spotify.com/documentation/general/guides/authorization/app-settings/

# imports
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


class SpotipyWrapper:
    def __init__(self) -> None:
        # get the required secrets from the environment variables
        self.client_id = os.environ.get("SPOTIPY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
        self.init_credential_manager()

    # connect to spotify using credential manager
    def init_credential_manager(self):
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    # function to get user's playlists
    def get_playlists(self, username):
        # get user's playlists
        playlists = self.sp.user_playlists(username)

        # print playlists
        for playlist in playlists["items"]:
            print(playlist["name"])
