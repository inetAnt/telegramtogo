#!/usr/bin/env python3
"""
telegramtogo
"""
import argparse
import json
import logging
import os
import time

import telegram
from tgtg import TgtgClient

from .utils import getLoggingLevel

AUTHOR = "Antoine Meillet"
AUTHOR_EMAIL = "antoine.meillet@gmail.com"
VERSION = "0.1.0"
LICENSE = "Apache-2.0"

LOGGING_LEVELS = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def main():
    """Main entry point of the app"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--email", default=os.environ.get("TGTG_EMAIL"))

    parser.add_argument("-cid", "--chat-id", default=os.environ.get("CHAT_ID"))
    parser.add_argument("-cto", "--chat-token", default=os.environ.get("CHAT_TOKEN"))

    parser.add_argument("-U", "--url", default=os.environ.get("URL"))

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=VERSION),
    )

    args = parser.parse_args()

    level = getLoggingLevel(args.verbose)
    logging.basicConfig(level=level)
    logging.debug("Logging level set to DEBUG")

    bot = telegram.Bot(args.chat_token)

    logging.debug("Reading credentials from JSON file")
    try:
        with open("credentials.json") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        credentials = None
        logging.debug("No token file exists")

    if not credentials:
        bot.send_message(
            chat_id=args.chat_id,
            text="Please open email to authenticate",
            parse_mode="Markdown",
        )
        client = TgtgClient(email=args.email)
        credentials = client.get_credentials()
        with open("credentials.json", "w") as f:
            json.dump(credentials, f)

    kwargs = credentials

    if args.url:
        kwargs["url"] = args.url

    client = TgtgClient(
        **kwargs,
    )

    previous_stock = set()

    while True:
        messages = []
        current_stock = client.get_items(page_size=400)

        for store in current_stock:
            item_id = store["item"]["item_id"]
            if store["items_available"] < 1:
                # drop from list if no more items
                if item_id in previous_stock:
                    logging.debug(f"removed item {item_id} from stock list")
                    previous_stock.remove(item_id)
                continue
            if item_id in previous_stock:
                logging.debug(
                    f"item {item_id} already in stock list, user already notified"
                )
                continue

            message = f"*{store['display_name']}*\n→ {store['items_available']} item(s) available"
            messages.append(message)
            logging.info(message)
            logging.debug(f"(re)adding {item_id} to stock list")
            previous_stock.add(item_id)
        if messages:
            bot.send_message(
                chat_id=args.chat_id, text="\n\n".join(messages), parse_mode="Markdown"
            )
        time.sleep(60)


if __name__ == "__main__":
    """This is executed when ran from the command line"""
    main()
