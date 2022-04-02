# Package to connect to Spotify API and retrieve data
# This package assumes you have a Spotify API client_id and client_secret
# in your environment variables.
# SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI
# See https://developer.spotify.com/documentation/general/guides/authorization/app-settings/

# imports
import os
import json
import datetime
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from logger import LOGGER


class SpotipyWrapper:
    def __init__(self, username) -> None:
        # get the required secrets from the environment variables
        self.client_id = os.environ.get("SPOTIPY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
        self.playlist_store = {}
        self.playlist_store = {"creation_date": "", "username": "", "playlists": {}}
        self.username = username
        self.init_credential_manager()

    def timestamp_now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # connect to spotify using credential manager
    def init_credential_manager(self):
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    # function to get user's playlists
    def get_playlists(self):
        # get user's playlists
        LOGGER.debug("Getting user's playlists")
        playlists = self.sp.user_playlists(self.username)

        return playlists["items"]

    # convert a playlist to a list of tracks
    def playlist_to_tracks(self, playlist_id):
        # get playlist's tracks
        LOGGER.debug("Getting playlist's tracks")
        playlist_tracks = self.sp.user_playlist_tracks(playlist_id=playlist_id)

        # get the tracks
        tracks = playlist_tracks["items"]

        # get the next tracks
        while playlist_tracks["next"]:
            playlist_tracks = self.sp.next(playlist_tracks)
            tracks.extend(playlist_tracks["items"])

        # return the tracks
        return tracks

    # collect tracks from playlists and prepare json structure
    def create_playlist_store(self):
        # get the user's playlists
        playlists = self.get_playlists()

        # create a collection of playlists
        self.playlist_store = {
            "creation_date": self.timestamp_now(),
            "username": self.username,
            "playlists": {},
        }

        playlist_dict_parent = {}

        # iterate through the playlists
        for playlist in playlists:
            # get the playlist's tracks
            LOGGER.info(f"Fetching details of playlist - {playlist['name']}")
            tracks = self.playlist_to_tracks(playlist["id"])

            # create a list of tracks
            track_list = []

            # iterate through the tracks
            for track in tracks:
                if track["track"] != None and track["track"]["id"] != None:
                    # get the track's data
                    track_data = self.sp.track(track["track"]["id"])

                    # create a dictionary of track data
                    track_dict = {
                        "name": track_data["name"],
                        "artist": track_data["artists"][0]["name"],
                        "album": track_data["album"]["name"],
                        "uri": track_data["uri"],
                        "duration": track_data["duration_ms"],
                    }

                    # add the track to the list
                    track_list.append(track_dict)

            # create a playlist dictionary
            playlist_dict = {
                "name": playlist["name"],
                "id": playlist["id"],
                "uri": playlist["uri"],
                "count": playlist["tracks"]["total"],
                "tracks": track_list,
            }

            # add the playlist to the list
            playlist_dict_parent[playlist["name"]] = playlist_dict

            if len(playlist_dict_parent) > 2:
                break

        # return the list of playlists
        self.playlist_store["playlists"] = playlist_dict_parent

    # function to accept a path and archive the folder
    def archive_playlist_store(self, path):
        # get the username and creation date
        username = self.playlist_store["username"]
        creation_date = self.playlist_store["creation_date"]

        # archive the folder
        os.system(f"tar -cvf {username}_{creation_date}.tar.gz ./{path}")

    # accept json dictionary and write to file
    def write_playlist_store(self):
        username = self.playlist_store["username"]
        creation_date = self.playlist_store["creation_date"]

        # create a directory for the user with timestamp
        os.system(f"mkdir {username}_{creation_date}")

        # write the playlist store to a file
        for pname, playlist in self.playlist_store["playlists"].items():
            with open(f"{username}_{creation_date}/{pname}.json", "w") as f:
                json.dump(playlist, f)

        # create an archive of downloaded playlists
        self.archive_playlist_store(f"{username}_{creation_date}")

        # delete original folder
        os.system(f"rm -rf {username}_{creation_date}")

    # read from file and display the playlists
    def read_playlist_store(self):
        # read the playlist store from a file
        with open("playlist_store.json", "r") as f:
            playlist_store = json.load(f)

        # display the playlists
        for playlist in playlist_store["playlists"]:
            print(playlist["name"])
            for track in playlist["tracks"]:
                print(
                    "  "
                    + track["name"]
                    + " - "
                    + track["artist"]
                    + " - "
                    + track["album"]
                )

    # display playlist store in json format
    # open in browser to view
    def display_playlist_store(self):
        # read the playlist store from a file
        with open("playlist_store.json", "r") as f:
            playlist_store = json.load(f)

        # display the playlists
        print(json.dumps(playlist_store, indent=4))

        # open the playlist store in the browser
        os.system(f"open {playlist_store['uri']}")
