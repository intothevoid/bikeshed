import os
import apprise
from util.config import load_config
from util.log import LOGGER

SETTINGS = load_config()


def get_env_var(var: str):
    """Get environment variable."""
    try:
        return os.environ[var]
    except KeyError:
        LOGGER.error(f"Environment variable {var} not set")
        return None


# Read settings
GOTIFY_URL = SETTINGS["GOTIFY_URL"] or get_env_var("GOTIFY_URL") or "localhost"
GOTIFY_TOKEN = SETTINGS["GOTIFY_TOKEN"] or get_env_var("GOTIFY_TOKEN") or ""
TELEGRAM_TOKEN = SETTINGS["TELEGRAM_TOKEN"] or get_env_var("TELEGRAM_TOKEN") or ""
TELEGRAM_CHAT_ID = SETTINGS["TELEGRAM_CHAT_ID"] or get_env_var("TELEGRAM_CHAT_ID") or ""

APR = apprise.Apprise()
APR_GOTIFY = "gotify://" + GOTIFY_URL + "/" + GOTIFY_TOKEN
APR_TELEGRAM = "tgram://" + TELEGRAM_TOKEN + "/" + TELEGRAM_CHAT_ID + "/"


def init_notification():
    try:
        if SETTINGS["ENABLE_NOTIFICATIONS"]:
            if "gotify" in SETTINGS["NOTIFICATION_TYPES"]:
                if GOTIFY_URL and GOTIFY_TOKEN:
                    APR.add(APR_GOTIFY)
                else:
                    LOGGER.error(
                        "GOTIFY_URL and GOTIFY_TOKEN settings must be set to use gotify notifications"
                    )
            if "telegram" in SETTINGS["NOTIFICATION_TYPES"]:
                if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
                    APR.add(APR_TELEGRAM)
                else:
                    LOGGER.error(
                        "TELEGRAM_TOKEN and TELEGRAM_CHAT_ID settings must be set to use telegram notifications"
                    )
    except Exception as exc:
        LOGGER.error(f"Error initialising notification system: {exc}")


def send_notification(message: str, title: str = "motogp-dl"):
    try:
        # Send notification
        APR.notify(body=message, title=title)
    except Exception as exc:
        LOGGER.error(f"Send notification error: {exc}")
