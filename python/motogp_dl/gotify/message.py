import os
import requests
from util.log import LOGGER


# send message via gotify
def send_gotify_message(message: str, title: str = "motogp_dl"):
    """
    This function sends a message to gotify via the gotify API.
    """
    # get gotify token from environment variable
    gotify_token = os.environ.get("GOTIFY_TOKEN")
    # get gotify url from environment variable
    gotify_url = os.environ.get("GOTIFY_URL")
    # get gotify app id from environment variable
    gotify_app_id = os.environ.get("GOTIFY_APP_ID")

    # check if gotify token, url and app id are set
    if gotify_token is None or gotify_url is None or gotify_app_id is None:
        LOGGER.error(
            "GOTIFY_TOKEN, GOTIFY_URL and GOTIFY_APP_ID environment variables must be set"
        )

    # create gotify message payload
    payload = {"message": message, "priority": 5, "title": title, "extras": None}

    # send message to gotify
    try:
        requests.post(
            f"{gotify_url}/message?token={gotify_token}&app={gotify_app_id}",
            json=payload,
        )
    except requests.exceptions.ConnectionError as exc:
        LOGGER.error(f"Error sending message to gotify: {exc}")
