#!/usr/bin/env python3
"""
telegramtogo
"""
import argparse
import logging
import os
import time


import telegram
from tgtg import TgtgClient

from .utils import getLoggingLevel

AUTHOR = "Antoine Meillet"
AUTHOR_EMAIL = "antoine.meillet@gmail.com"
VERSION = "0.0.1"
LICENSE = "Apache-2.0"

LOGGING_LEVELS = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def main():
    """ Main entry point of the app """
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--username", default=os.environ.get("USERNAME"))
    parser.add_argument("-p", "--password", default=os.environ.get("PASSWORD"))

    parser.add_argument("-id", "--user-id", default=os.environ.get("USER_ID"))
    parser.add_argument("-t", "--token", default=os.environ.get("TOKEN"))

    parser.add_argument("-cid", "--chat-id", default=os.environ.get("CHAT_ID"))
    parser.add_argument("-cto", "--chat-token", default=os.environ.get("CHAT_TOKEN"))
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

    if args.username and args.password:
        auth = {
            "email": args.username,
            "password": args.password,
        }
    elif args.user_id and args.token:
        auth = {"access_token": args.token, "user_id": args.user_id}
    else:
        raise ValueError("no authentication provided")

    level = getLoggingLevel(args.verbose)
    logging.basicConfig(level=level)
    logging.debug("Logging level set to DEBUG")

    logging.info(f"Connecting with username: {args.username}")
    client = TgtgClient(
        user_agent="TooGoodToGo/20.3.1 (759) (iPhone/iPhone 7; iOS 13.0; Scale/2.00)",
        **auth,
    )

    bot = telegram.Bot(args.chat_token)

    previous_stock = set()

    while True:
        current_stock = client.get_items()

        for store in current_stock:
            store_id = store["store"]["store_id"]
            if store["items_available"] < 1:
                # drop from list if no more items
                if store_id in previous_stock:
                    logging.debug(f"removed store {store_id} from stock list")
                    previous_stock.remove(store_id)
                continue
            if store_id in previous_stock:
                logging.debug(
                    f"store {store_id} already in stock list, user already notified"
                )
                continue

            message = f"*{store['display_name']}*\n→ {store['items_available']} item(s) available"
            logging.info(message)
            bot.send_message(chat_id=args.chat_id, text=message, parse_mode="Markdown")
            logging.debug(f"(re)adding {store_id} to stock list")
            previous_stock.add(store_id)
            time.sleep(0.2)
        time.sleep(60)


if __name__ == "__main__":
    """ This is executed when ran from the command line """
    main()
