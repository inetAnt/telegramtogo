from setuptools import setup

from telegramtogo.telegramtogo import AUTHOR, AUTHOR_EMAIL, VERSION, LICENSE

setup(
    name="telegramtogo",
    version=VERSION,
    description="Telegram bot for TooGoodToGo",
    url="http://github.com/inetant/telegramtogo",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=["telegramtogo"],
    zip_safe=False,
    entry_points={"console_scripts": ["telegramtogo=telegramtogo.telegramtogo:main"]},
)
