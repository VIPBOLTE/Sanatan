import logging  
import os
from pyrogram import Client 
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

from config import *


API_ID = API_ID
API_HASH = API_HASH
BOT_TOKEN = BOT_TOKEN
LOGGER_ID = LOGGER_ID
MONGO_DB_URI = MONGO_DB_URI
VIDEO_URL = VIDEO_URL 
SUPPORT_CHAT = SUPPORT_CHAT 
SUPPORT_CHANNEL= SUPPORT_CHANNEL
BOT_USERNAME = BOT_USERNAME 
sudo_users = sudo_users
OWNER_ID = OWNER_ID 

from Config import development as Config

sudo_users = Config.sudo_users
application = Application.builder().token(BOT_TOKEN).build()
Sanatan = Client("Sanatan", API_ID, API_HASH, bot_token=BOT_TOKEN)
lol = AsyncIOMotorClient(MONGO_DB_URI)
db = lol['Character_catcher']
collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
