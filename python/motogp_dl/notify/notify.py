import apprise
from util.config import load_config
from util.log import LOGGER

SETTINGS = load_config()

# Read settings
GOTIFY_URL = SETTINGS["GOTIFY_URL"]
GOTIFY_TOKEN = SETTINGS["GOTIFY_TOKEN"]
TELEGRAM_TOKEN = SETTINGS["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = SETTINGS["TELEGRAM_CHAT_ID"]

APR = apprise.Apprise()
APR_GOTIFY = "gotify://" + GOTIFY_URL + "/" + GOTIFY_TOKEN
APR_TELEGRAM = "tgram://" + TELEGRAM_TOKEN + "/" + TELEGRAM_CHAT_ID + "/"


def send_notification(message: str, title: str = "motogp-dl"):
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

            # Send notification
            APR.notify(body=message, title=title)
    except Exception as exc:
        LOGGER.error(f"Send notification error: {exc}")
