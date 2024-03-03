import logging
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from Sanatan import application, db

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
            if last_claimed and datetime.now() - last_claimed < timedelta(days=1):
                await update.message.reply_text("You have already claimed your daily reward.")
                return

            await add_coins(user_id, 40)
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
            if last_claimed and datetime.now() - last_claimed < timedelta(weeks=1):
                await update.message.reply_text("You have already claimed your weekly reward.")
                return

            await add_coins(user_id, 250)
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
        else:
            await wallet_collection.insert_one({"user_id": user_id, "coins": 250, "last_weekly_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

# Command handlers
CHECK_BALANCE_HANDLER = CommandHandler('balance', check_balance)
application.add_handler(CHECK_BALANCE_HANDLER)

DAILY_REWARD_HANDLER = CommandHandler('daily', daily_reward)
application.add_handler(DAILY_REWARD_HANDLER)

WEEKLY_REWARD_HANDLER = CommandHandler('weekly', weekly_reward)
application.add_handler(WEEKLY_REWARD_HANDLER)
