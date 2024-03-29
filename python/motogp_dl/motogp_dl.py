import os
import sys
from datetime import date

# Add the root folder to the module search path
root_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_folder)

import datetime
import psutil
import contextlib
import feedparser
import re
import subprocess
import time
from notify.notify import send_notification, init_notification
from util.log import LOGGER
from util.config import load_config
from util.validity import check_valid_dl_type

# Global variable to store the count of downloads
download_count = 0
last_download_date = date.today()

# Settings
try:
    SETTINGS = load_config()
    FEEDURL = SETTINGS["FEED"] or "https://www.reddit.com/r/MotorsportsReplays.rss"
    DOWNLOAD_DIR = SETTINGS["DOWNLOAD_DIR"] or "./downloads"
    INTERVAL_MINS = SETTINGS["INTERVAL_MINS"] or 60  # example: 5
    DELETE_OLD_FILES = SETTINGS["DELETE_OLD_FILES"] or True  # example: True
    DELETE_OLD_FILES_THRESHOLD = (
        SETTINGS["DELETE_OLD_FILES_THRESHOLD"] or 10
    )  # example: 10
    MAX_DOWNLOADS_PER_DAY = SETTINGS["MAX_DOWNLOADS_PER_DAY"] or 1  # example: 1

except KeyError as exc:
    LOGGER.error(f"KeyError: {exc}")

# Notification settings
# If you wish to use gotify, you need to set the following environment variables:
# GOTIFY_URL, GOTIFY_APP_ID and GOTIFY_TOKEN


# Iterate over the entries and extract magnet links
def parse_feed(latest: bool = True):
    """This function parses the RSS feed and downloads the torrents.
    It looks for titles using positive and negative filters.
    It checks if the torrent has already been downloaded and skips it if so.
    It then downloads the torrent using aria2 and adds the torrent to the downloaded.txt file.
     Args:
        latest (bool): If True, only the latest torrent is downloaded.
     Returns:
        None
    """
    global download_count

    LOGGER.info(
        f"Filters set - POSITIVE_FILTERS: {SETTINGS['POSITIVE_FILTERS']}, NEGATIVE_FILTERS: {SETTINGS['NEGATIVE_FILTERS']}"
    )

    # Parse data using RSS library
    try:
        FEED = feedparser.parse(FEEDURL)
    except Exception as exc:
        LOGGER.error(f"Error parsing feed: {exc}")

    for entry in FEED.entries:
        LOGGER.info(f"Checking entry: {entry.title}")

        # Check if entry is valid
        isTitleValid: bool = check_valid_dl_type(entry.title, SETTINGS)

        if isTitleValid:
            # Extract magnet link from content
            match = re.search(r"magnet:\?xt=urn:btih:\w+", entry.content[0].value)
            if match:
                magnet_link = match.group(0)
                LOGGER.info(f"Found magnet link:{entry.title} - {magnet_link}")

                if already_downloaded(magnet_link):
                    LOGGER.info(f"Already downloaded - skipping: {magnet_link}")
                    continue

                if max_downloads_per_day_reached(MAX_DOWNLOADS_PER_DAY):
                    LOGGER.info(
                        f"Max downloads per day reached - skipping: {magnet_link}"
                    )
                    continue

                # Send notification
                send_notification(f"Found new video: {entry.title} - {magnet_link}")

                # check disk space, delete oldest file if below threshold until above threshold
                while is_disk_space_below_threshold(DELETE_OLD_FILES_THRESHOLD):
                    LOGGER.warning(f"Disk space below threshold - deleting oldest file")
                    delete_oldest_file()

                    time.sleep(15)  # sleep for 15 seconds, wait for file to be deleted

                try:
                    # Pass magnet link to aria2 via command line
                    LOGGER.info(f"Downloading: {magnet_link} via aria2")
                    ret = run_aria2c(magnet_link)
                    # process return code
                    if ret.returncode == 0:
                        LOGGER.info(f"Downloaded: {magnet_link}")
                        send_notification(f"Downloaded: {entry.title}")
                        download_count += 1
                    elif ret.returncode == 13 or ret.returncode == 11:
                        LOGGER.info(f"File already exists or is being downloaded")
                        if latest:
                            break
                        else:
                            continue
                    else:
                        send_notification(f"Error downloading: {magnet_link}")
                        LOGGER.error(f"Error downloading: {magnet_link}")
                        continue
                except FileNotFoundError as exc:
                    LOGGER.error(f"aria2c not found {exc}")
                    send_notification(f"aria2c not found {exc}")
                    if latest:
                        break
                    else:
                        continue

                # record magnet link to file as downloaded
                with open(f"{DOWNLOAD_DIR}/downloaded.txt", "a") as f:
                    with contextlib.suppress(Exception):
                        f.write(f"{magnet_link}\n")

                # break out if we have downloaded the latest
                if latest:
                    break

                # avoid tightloop
                time.sleep(1)


def run_aria2c(magnet_link):
    """
    This function runs aria2c via the command line.
    It takes in a magnet link as a parameter and then runs aria2c with the magnet link.
    """
    ret = subprocess.run(
        [
            "aria2c",
            "--listen-port",
            "6881-6885",
            "--disable-ipv6=true",
            "--seed-time=0",
            "-d",
            f"{DOWNLOAD_DIR}",
            magnet_link,
        ],
        check=True,
    )

    return ret


def already_downloaded(magnet_link: str) -> bool:
    """
    This function checks if a magnet link has already been downloaded.
    It reads in the magnet link as a parameter and then searches through the downloaded.txt file
    to see if the link is in there. If it finds the link it will return True, otherwise it will
    return False. If the file does not exist it will skip it and return False."""
    try:
        with open(f"{DOWNLOAD_DIR}/downloaded.txt", "r") as f:
            for line in f.readlines():
                if magnet_link in line:
                    return True
    except FileNotFoundError:
        # create empty file if it doesn't exist
        with open(f"{DOWNLOAD_DIR}/downloaded.txt", "w") as f:
            pass

    return False


def is_disk_space_below_threshold(threshold: int = DELETE_OLD_FILES_THRESHOLD):
    """This function checks the disk space of the download directory.
    If the disk space is less than 10GB it will delete the oldest file in the directory.
    """
    disk_usage = psutil.disk_usage("/")
    disk_space = f"{disk_usage.free / (2**30):.1f} GB"  # calculate free space in GB and format as string
    free_space_in_gb = float(disk_space[:-3])
    return int(free_space_in_gb) < threshold


def delete_oldest_file():
    """
    This function deletes the oldest file in the download directory.
    """
    if not DELETE_OLD_FILES:
        return

    # get oldest file in directory
    files = subprocess.run(
        ["ls", "-t", f"{DOWNLOAD_DIR}"], capture_output=True
    ).stdout.decode("utf-8")
    oldest_file = files.split("\n")[-2]

    # delete oldest file
    subprocess.run(["rm", f"{DOWNLOAD_DIR}/{oldest_file}"])


def max_downloads_per_day_reached(max_downloads: int) -> bool:
    global download_count
    global last_download_date

    # Check if the date has changed since the last download
    if date.today() != last_download_date:
        # If the date has changed, reset the download count and update the last download date
        download_count = 0
        last_download_date = date.today()

    if download_count >= max_downloads:
        return True
    else:
        return False


# Call parse_feed() every INTERVAL_MINS minutes
if __name__ == "__main__":
    curr_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    LOGGER.info(f"Starting MotoGP Downloader v1.0. Time: {curr_date}")
    init_notification()
    send_notification(f"Starting MotoGP Downloader v1.0. Time: {curr_date}")

    # check feed every INTERVAL_MINS minutes
    while True:
        LOGGER.info("Parsing reddit.com/r/MotorsportsReplays feed for new content")
        try:
            parse_feed(True)
        except Exception as exc:
            LOGGER.error(f"Error parsing feed: {exc}")
            send_notification(f"Error parsing feed: {exc}")
            sys.exit(1)
        time.sleep(60 * INTERVAL_MINS)  # interval in mins
