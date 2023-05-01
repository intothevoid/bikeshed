import feedparser
import re
import subprocess
import time

# Settings
FEED = feedparser.parse("https://www.reddit.com/r/MotorsportsReplays.rss")
DOWNLOAD_DIR = "/home/rtorrent/downloads"
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
                    # Pass magnet link to rtorrent via command line
                    subprocess.run(
                        ["rtorrent", "-q", "-d", f"{DOWNLOAD_DIR}", magnet_link]
                    )
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
    try:
        with open("downloaded.txt", "r") as f:
            for line in f.readlines():
                if magnet_link in line:
                    return True
    except FileNotFoundError:
        pass

    return False


# Call parse_feed() every INTERVAL_MINS minutes
if __name__ == "__main__":
    while True:
        parse_feed(True)
        time.sleep(60 * INTERVAL_MINS)  # interval in mins
