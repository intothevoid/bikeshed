import argparse
from spotipywrapper.helper import SpotipyWrapper
from logger import LOGGER, configure_logging

# backup spotify playlists
def backup_spotify_playlists(username):
    LOGGER.info("Backup spotify playlists")
    sw = SpotipyWrapper(username)
    sw.init_credential_manager()
    sw.create_playlist_store()
    sw.write_playlist_store()


# restore spotify playlists
def restore_spotify_playlists(username):
    LOGGER.info("Restore spotify playlists")
    sw = SpotipyWrapper()
    sw.init_credential_manager()
    sw.read_playlist_store()
    # spotify.create_playlists()


# parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Backup or restore spotify playlists")
    parser.add_argument("-u", "--username", help="Spotify username", required=True)
    parser.add_argument(
        "-b", "--backup", help="Backup spotify playlists", action="store_true"
    )
    parser.add_argument(
        "-r", "--restore", help="Restore spotify playlists", action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    # accept arguments --username, --backup, --restore
    # if no arguments, display help message
    # if --username, get the user's playlists
    # if --backup, get the user's playlists and write to file
    # if --restore, read from file and display the playlists

    # configure logging
    configure_logging()

    # parse the arguments
    LOGGER.info("Parsing arguments")
    args = parse_args()

    if args.username:
        if args.backup:
            backup_spotify_playlists(args.username)
        elif args.restore:
            restore_spotify_playlists(args.username)
        else:
            LOGGER.error("No arguments specified")
    else:
        LOGGER.error("No username specified")
