from spotipywrapper.helper import SpotipyWrapper

# main function
def main():
    # create a SpotifyWrapper object
    spotify = SpotipyWrapper()

    # get the user's playlists
    # ask the user for a username
    username = input("Enter a username: ")
    playlists = spotify.get_playlists(username)

    # print the playlists
    for playlist in playlists:
        print(playlist["name"])


if __name__ == "__main__":
    main()
