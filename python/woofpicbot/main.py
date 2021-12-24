from telegram import update
from telegram.ext import Updater, CommandHandler
import requests
import re
import os

URL = "https://random.dog/woof.json"


def get_url():
    contents = requests.get(URL).json()
    url = contents["url"]
    return url


def woof(update, context):
    url = get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def main():
    token_id = os.environ["TELEGRAM_WOOF_TOKEN"] or "NA"
    updater = Updater(token=token_id, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("woof", woof))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
