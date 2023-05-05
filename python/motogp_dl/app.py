import contextlib
import logging
import feedparser
import re
import subprocess
import time

# Settings
FEED = feedparser.parse("https://www.reddit.com/r/MotorsportsReplays.rss")
DOWNLOAD_DIR = "/downloads"
QUALITY = "1080"
INTERVAL_MINS = 60  # minutes
DELETE_OLD_FILES = True
DELETE_OLD_FILES_THRESHOLD = 10  # GB

# setup logging
logging.basicConfig(
    filename=f"app.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


# Iterate over the entries and extract magnet links
def parse_feed(latest: bool = True):
    """This function parses the RSS feed and downloads the torrents.
    It looks for titles with 'motogp' and the specified quality or 'HD'.
    It checks if the torrent has already been downloaded and skips it if so.
    It then downloads the torrent using aria2 and adds the torrent to the downloaded.txt file.
     Args:
        latest (bool): If True, only the latest torrent is downloaded.
     Returns:
        None
    """
    for entry in FEED.entries:
        if "motogp" in entry.title.lower() and (
            f"{QUALITY}" in entry.title.lower() or "hd" in entry.title.lower()
        ):
            # Extract magnet link from content
            match = re.search(r"magnet:\?xt=urn:btih:\w+", entry.content[0].value)
            if match:
                magnet_link = match.group(0)
                LOGGER.info(f"Found magnet link:{entry.title} - {magnet_link}")

                if already_downloaded(magnet_link):
                    LOGGER.info(f"Already downloaded - skipping: {magnet_link}")
                    continue

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
                    else:
                        LOGGER.error(f"Error downloading: {magnet_link}")
                        continue
                except FileNotFoundError as exc:
                    LOGGER.error(f"aria2c not found {exc}")
                    if latest:
                        break
                    else:
                        continue

                # record magnet link to file as downloaded
                with open("downloaded.txt", "a") as f:
                    with contextlib.suppress(Exception):
                        f.write(f"{magnet_link}\n")

                # break out if we have downloaded the latest
                if latest:
                    break

            LOGGER.info(f"Downloaded {magnet_link}")


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
        with open("downloaded.txt", "r") as f:
            for line in f.readlines():
                if magnet_link in line:
                    return True
    except FileNotFoundError:
        # create empty file if it doesn't exist
        with open("downloaded.txt", "w") as f:
            pass

    return False


def is_disk_space_below_threshold(threshold: int = DELETE_OLD_FILES_THRESHOLD) -> bool:
    """This function checks the disk space of the download directory.
    If the disk space is less than 10GB it will delete the oldest file in the directory.
    """
    # get disk space
    df = subprocess.run(["df", "-h", f"{DOWNLOAD_DIR}"], capture_output=True)
    disk_space = df.stdout.decode("utf-8").split("\n")[1].split()[3]

    # check if disk space is less than threshold
    if int(disk_space[:-1]) < threshold:
        return True

    return False


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


# Call parse_feed() every INTERVAL_MINS minutes
if __name__ == "__main__":
    while True:
        parse_feed(True)
        time.sleep(60 * INTERVAL_MINS)  # interval in mins
