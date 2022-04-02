# test cases for application

# imports
import os
import spotipy
import unittest


class SpottyTests(unittest.TestCase):
    def test_get_client_id_from_env():
        # get client id from enviroment variable
        client_id = os.environ.get("SPOTIFY_CLIENT_ID")

        # return client id
        assert client_id != None
        assert client_id != ""

    def test_get_client_secret_from_env():
        # get client secret from enviroment variable
        client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

        # return client secret
        assert client_secret != None
        assert client_secret != ""
