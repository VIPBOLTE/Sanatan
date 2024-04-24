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
OWNER_USERNAME = getenv("OWNER_USERNAME", "Zindagi_hai_tere_nal")
#bot ko jiske liye bna rha wo hai DEVELOP without @
DEVELOP = getenv(" DEVELOP","")
# Get Your bot username
BOT_USERNAME = getenv("BOT_USERNAME", "Husbandobot")
# Don't Add style font 
BOT_NAME = getenv("NAME", "GOKU_WAIFUS")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://sanasomani786:TJgADfpkI1XVUkKt@cluster0.ruhyad9.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")


VIDEO_URL = getenv(
    "START_IMG_URL"," https://telegra.ph/file/2f56b2568b3f92abcf55e.mp4") 

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", "-1002126989582"))

# Get this value from  on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "5595153270"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/VIPBOLTE/Sanatan",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "channelz_k")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "goku_groupz") 

sudo_users = "5595153270", "6092692622"

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}






       
