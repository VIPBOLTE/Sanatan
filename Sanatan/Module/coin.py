import random
import html
import logging 
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from Sanatan import application, db
from Sanatan import (application, PHOTO_URL, OWNER_ID,
                    user_collection, top_global_groups_collection, top_global_groups_collection, 
                    group_user_totals_collection)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

wallet_collection = db["user_wallets"]

async def check_balance(update: Update, context: CallbackContext) -> None:
    try:
        user_id = str(update.effective_user.id)
        user_wallet = await wallet_collection.find_one({"user_id": user_id})

        if user_wallet:
            coins = user_wallet.get("coins", 0)
            await update.message.reply_text(f"Your current balance: {coins} coins.")
        else:
            await update.message.reply_text("You don't have any coins yet.")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

async def add_coins(user_id: str, amount: int) -> None:
    try:
        user_wallet = await wallet_collection.find_one({"user_id": user_id})

        if user_wallet:
            current_coins = user_wallet.get("coins", 0)
            await wallet_collection.update_one(
                {"user_id": user_id},
                {"$set": {"coins": current_coins + amount}},
            )
        else:
            await wallet_collection.insert_one({"user_id": user_id, "coins": amount})
    except Exception as e:
        LOGGER.error(f"Error adding coins: {e}")

async def daily_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = str(update.effective_user.id)
        user_wallet = await wallet_collection.find_one({"user_id": user_id})

        if user_wallet:
            last_claimed = user_wallet.get("last_daily_claimed")
            if last_claimed and last_claimed.date() == datetime.now().date():
                await update.message.reply_text("You have already claimed your daily reward.")
                return

            await add_coins(user_id, 40)
            await wallet_collection.update_one(
                {"user_id": user_id},
                {"$set": {"last_daily_claimed": datetime.now()}},
            )
            await update.message.reply_text("You have claimed your daily reward. You earned 40 coins.")
        else:
            await wallet_collection.insert_one({"user_id": user_id, "coins": 40, "last_daily_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your daily reward. You earned 40 coins.")
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text(f"Error occurred: {e}")



async def weekly_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = str(update.effective_user.id)
        user_wallet = await wallet_collection.find_one({"user_id": user_id})

        if user_wallet:
            last_claimed = user_wallet.get("last_weekly_claimed")
            start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
            if last_claimed and last_claimed.date() >= start_of_week:
                await update.message.reply_text("You have already claimed your weekly reward.")
                return

            await add_coins(user_id, 250)
            await wallet_collection.update_one(
                {"user_id": user_id},
                {"$set": {"last_weekly_claimed": datetime.now()}},
            )
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
        else:
            await wallet_collection.insert_one({"user_id": user_id, "coins": 250, "last_weekly_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text(f"Error occurred: {e}")
        
async def top_users_by_coins(update: Update, context: CallbackContext) -> None:
    cursor = wallet_collection.aggregate([
        {"$project": {"user_id": 1, "coins": 1}},
        {"$sort": {"coins": -1}},
        {"$limit": 10}
    ])
    top_users_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>TOP 10 USERS WITH MOST COINS</b>\n\n"

    for i, user_data in enumerate(top_users_data, start=1):
        user_id = user_data.get('user_id', 'Unknown')
        coins = user_data.get('coins', 0)

        try:
            user = await context.bot.get_chat(user_id)
            username = user.username if user.username else user.first_name
            leaderboard_message += f"{i}. <a href=\"https://t.me/{username}\"><b>{username}</b></a> ➾ <b>{coins}</b>\n"

        except Exception as e:
            LOGGER.error(f"Error getting user info: {e}")
    
    photo_url = random.choice(PHOTO_URL)
    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')


# Command handlers
CHECK_BALANCE_HANDLER = CommandHandler('balance', check_balance)
application.add_handler(CHECK_BALANCE_HANDLER)

DAILY_REWARD_HANDLER = CommandHandler('daily', daily_reward)
application.add_handler(DAILY_REWARD_HANDLER)

WEEKLY_REWARD_HANDLER = CommandHandler('weekly', weekly_reward)
application.add_handler(WEEKLY_REWARD_HANDLER)

TOPS_HANDLER = CommandHandler('cointop', top_users_by_coins, block=False)
application.add_handler(TOPS_HANDLER)
