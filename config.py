import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")
# Add Owner Username without @ 
OWNER_USERNAME = getenv("OWNER_USERNAME", "roy_editx")
# Get Your bot username
BOT_USERNAME = getenv("BOT_USERNAME", "NykaaxBot")
# Don't Add style font 
BOT_NAME = getenv("NAME", "")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://sanasomani786:TJgADfpkI1XVUkKt@cluster0.ruhyad9.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")



# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", "-1001929735324"))

# Get this value from  on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "6195725562"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/VIPBOLTE/SANATAN",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "mean")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/channelz_k")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/goku_groupz") 



BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}






if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
)
