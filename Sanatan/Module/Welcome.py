import urllib.request
from pymongo import ReturnDocument
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from Sanatan import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

wallet_collection = db["user_wallets"]

RARITY_COIN_MAP = {
    " ⚪️ Common": 30,
    "🟣 Rare": 45,
    "🟡 Legendary": 100,
    "🟢 Medium": 60,
    "💮 Special edition": 130,
    "🔮 Limited Edition": 180,
}

async def daily_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = str(update.effective_user.id)
        user_wallet = wallet_collection.find_one({"user_id": user_id})

        if user_wallet:
            # Check if the user has claimed daily reward in the last 24 hours
            last_claimed = user_wallet.get("last_daily_claimed")
            if last_claimed and datetime.now() - last_claimed < timedelta(days=1):
                await update.message.reply_text("You have already claimed your daily reward.")
                return

            # Update user's coins for daily reward
            current_coins = user_wallet.get("coins", 0)
            wallet_collection.update_one(
                {"user_id": user_id},
                {"$set": {"coins": current_coins + 40, "last_daily_claimed": datetime.now()}},
            )
            await update.message.reply_text("You have claimed your daily reward. You earned 40 coins.")
        else:
            # Create new user wallet if not exists
            wallet_collection.insert_one({"user_id": user_id, "coins": 40, "last_daily_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your daily reward. You earned 40 coins.")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

# Function to handle weekly reward
async def weekly_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = str(update.effective_user.id)
        user_wallet = wallet_collection.find_one({"user_id": user_id})

        if user_wallet:
            # Check if the user has claimed weekly reward in the last 7 days
            last_claimed = user_wallet.get("last_weekly_claimed")
            if last_claimed and datetime.now() - last_claimed < timedelta(weeks=1):
                await update.message.reply_text("You have already claimed your weekly reward.")
                return

            # Update user's coins for weekly reward
            current_coins = user_wallet.get("coins", 0)
            wallet_collection.update_one(
                {"user_id": user_id},
                {"$set": {"coins": current_coins + 250, "last_weekly_claimed": datetime.now()}},
            )
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
        else:
            # Create new user wallet if not exists
            wallet_collection.insert_one({"user_id": user_id, "coins": 250, "last_weekly_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")




DAILY_REWARD_HANDLER = CommandHandler('daily', daily_reward, block=False)
application.add_handler(DAILY_REWARD_HANDLER)
WEEKLY_REWARD_HANDLER = CommandHandler('weekly', weekly_reward, block=False)
application.add_handler(WEEKLY_REWARD_HANDLER)
