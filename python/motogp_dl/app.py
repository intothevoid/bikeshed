import feedparser
import re
import subprocess
import time

# Settings
FEED = feedparser.parse("https://www.reddit.com/r/MotorsportsReplays.rss")
DOWNLOAD_DIR = "/downloads"
QUALITY = "1080"
INTERVAL_MINS = 60  # minutes


# Iterate over the entries and extract magnet links
def parse_feed(latest: bool = True):
    for entry in FEED.entries:
        if "motogp" in entry.title.lower() and (
            f"{QUALITY}" in entry.title.lower() or "hd" in entry.title.lower()
        ):
            # Extract magnet link from content
            match = re.search(r"magnet:\?xt=urn:btih:\w+", entry.content[0].value)
            if match:
                magnet_link = match.group(0)
                print(f"Found magnet link:{entry.title} - {magnet_link}")

                if already_downloaded(magnet_link):
                    print(f"Already downloaded - skipping: {magnet_link}")
                    continue

                try:
                    # Pass magnet link to aria2 via command line
                    print(f"Downloading: {magnet_link} via aria2")
                    ret = subprocess.run(
                        [
                            "aria2c",
                            "--listen-port",
                            "6881-6885",
                            "--disable-ipv6=true",
                            "-d",
                            f"{DOWNLOAD_DIR}",
                            magnet_link,
                        ]
                    )
                    # process return code
                    if ret.returncode == 0:
                        print(f"Downloaded: {magnet_link}")
                    else:
                        print(f"Error downloading: {magnet_link}")
                        continue
                except FileNotFoundError as exc:
                    print(f"rtorrent not found {exc}")
                    if latest:
                        break
                    else:
                        continue

                # record magnet link to file as downloaded
                with open("downloaded.txt", "a") as f:
                    f.write(f"{magnet_link}\n")

                # only fetch  the latest magnet link
                if latest:
                    break


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


# Call parse_feed() every INTERVAL_MINS minutes
if __name__ == "__main__":
    while True:
        parse_feed(True)
        time.sleep(60 * INTERVAL_MINS)  # interval in mins
