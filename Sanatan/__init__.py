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

from Sanatan.Config import Development as Config


API_ID= Config.API_ID
API_HASH= Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
GROUP_ID = Config.GROUP_ID
MONGO_URL= Config.MONGO_URL
VIDEO_URL = Config.VIDEO_URL 
SUPPORT_CHAT = Config.SUPPORT_CHAT 
SUPPORT_CHANNEL= Config.SUPPORT_CHANNEL
BOT_USERNAME = Config.BOT_USERNAME 
sudo_users = Config.sudo_users
OWNER_ID = Config.OWNER_ID 

application = Application.builder().bot_token(BOT_TOKEN).build()
Sanatan = Client("Sanatan", API_ID, API_HASH, bot_token=BOT_TOKEN)
lol = AsyncIOMotorClient(MONGO_URL)
db = lol['Character_catcher']
collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
