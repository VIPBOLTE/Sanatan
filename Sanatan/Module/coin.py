
import urllib.request
import uuid
import requests
import random
import html
import logging
from pymongo import ReturnDocument
from typing import List
from bson import ObjectId
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime, timedelta

# Assuming these are defined elsewhere in your code
from Sanatan import db, UPDATE_CHAT, SUPPORT_CHAT, CHARA_CHANNEL_ID, collection, user_collection
from Sanatan import (application, PHOTO_URL, OWNER_ID,
                    user_collection, top_global_groups_collection, top_global_groups_collection, 
                    group_user_totals_collection)

shops_collection = db["shops"]
# Owner ID
OWNER_ID = "6257270528"

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

WRONG_FORMAT_TXT = """Wrong ❌ format...  eg. /uploaded Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

use rarity number accordingly rarity Map

rarity_map = 1 (💸 Premium Edition)"""



async def check_balance(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(update.effective_user.id)
        user = await user_collection.find_one({"id": user_id})

        if user:
            coins = user.get("coins", 0)
            await update.message.reply_text(f"Your current balance: {coins} coins.")
        else:
            await update.message.reply_text("You don't have any coins yet.")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

async def add_coins(user_id: int, amount: int) -> None:
    try:
        user = await user_collection.find_one({"id": user_id})

        if user:
            current_coins = user.get("coins", 0)
            await user_collection.update_one(
                {"id": user_id},
                {"$set": {"coins": current_coins + amount}},
            )
        else:
            await user_collection.insert_one({"id": user_id, "coins": amount})
    except Exception as e:
        LOGGER.error(f"Error adding coins: {e}")

async def daily_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(update.effective_user.id)
        user = await user_collection.find_one({"id": user_id})

        if user:
            last_claimed = user.get("last_daily_claimed")
            if last_claimed and last_claimed.date() == datetime.now().date():
                await update.message.reply_text("You have already claimed your daily reward.")
                return

            await add_coins(user_id, 40)
            await user_collection.update_one(
                {"id": user_id},
                {"$set": {"last_daily_claimed": datetime.now()}},
            )
            await update.message.reply_text("You have claimed your daily reward. You earned 40 coins.")
        else:
            await user_collection.insert_one({"id": user_id, "coins": 40, "last_daily_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your daily reward. You earned 40 coins.")
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text(f"Error occurred: {e}")



async def weekly_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(update.effective_user.id)
        user = await user_collection.find_one({"id": user_id})

        if user:
            last_claimed = user.get("last_weekly_claimed")
            start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
            if last_claimed and last_claimed.date() >= start_of_week:
                await update.message.reply_text("You have already claimed your weekly reward.")
                return

            await add_coins(user_id, 250)
            await user_collection.update_one(
                {"id": user_id},
                {"$set": {"last_weekly_claimed": datetime.now()}},
            )
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
        else:
            await user_collection.insert_one({"id": user_id, "coins": 250, "last_weekly_claimed": datetime.now()})
            await update.message.reply_text("You have claimed your weekly reward. You earned 250 coins.")
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text(f"Error occurred: {e}")
        


async def top_users_by_coins(update: Update, context: CallbackContext) -> None:
    try:
        cursor = user_collection.aggregate([
            {"$project": {"id": 1, "coins": 1}},
            {"$sort": {"coins": -1}},
            {"$limit": 10}
        ])
        top_users_data = await cursor.to_list(length=10)

        leaderboard_message = "<b>TOP 10 USERS WITH MOST COINS</b>\n\n"

        for i, user_data in enumerate(top_users_data, start=1):
            user_id = user_data.get('id', 'Unknown')
            coins = user_data.get('coins', 0)

            try:
                user = await context.bot.get_chat(user_id)
                username = user.username if user.username else user.first_name
                display_name = user.title if user.title else user.first_name
                leaderboard_message += f"{i}. <a href=\"https://t.me/{username}\">{display_name}</a> - <b>{coins}</b>\n"

            except Exception as e:
                LOGGER.error(f"Error getting user info: {e}")
                continue  # Skip this user and proceed to the next one

        photo_url = random.choice(PHOTO_URL)
        await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while fetching top users by coins.")


async def remove_coins(update: Update, context: CallbackContext) -> None:
    try:
        if int(update.effective_user.id) != 6257270528:
            await update.message.reply_text("You are not authorized to perform this action.")
            return

        # Parse user_id and coins from the command arguments
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Invalid format. Use: /removecoins <user_id> <amount>")
            return

        user_id = args[0]
        try:
            amount = int(args[1])
        except ValueError:
            await update.message.reply_text("Invalid amount. Please provide a valid number.")
            return

        # Retrieve user's wallet
        user = await user_collection.find_one({"id": int(user_id)})

        if not user:
            await update.message.reply_text("User not found.")
            return

        current_balance = user.get("coins", 0)
        new_balance = max(0, current_balance - amount)

        # Update user's balance
        await user_collection.update_one({"id": int(user_id)}, {"$set": {"coins": new_balance}})

        await update.message.reply_text(f"Successfully removed {amount} coins from user {user_id}. New balance: {new_balance}")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while removing coins. Please try again later.")


async def give_coins(update: Update, context: CallbackContext) -> None:
    try:
        if int(update.effective_user.id) != 6257270528:
            await update.message.reply_text("You are not authorized to perform this action.")
            return

        # Parse user_id and coins from the command arguments
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Invalid format. Use: /givecoins <user_id> <amount>")
            return

        user_id = args[0]
        try:
            amount = int(args[1])
        except ValueError:
            await update.message.reply_text("Invalid amount. Please provide a valid number.")
            return

        # Retrieve user's wallet
        user = await user_collection.find_one({"id": int(user_id)})

        if not user:
            # Initialize user's wallet if it doesn't exist
            await user_collection.insert_one({"id": int(user_id), "coins": amount})
            await update.message.reply_text(f"User {user_id} didn't have a wallet. Initialized with {amount} coins.")
            return

        current_balance = user.get("coins", 0)
        new_balance = current_balance + amount

        # Update user's balance
        await user_collection.update_one({"id": int(user_id)}, {"$set": {"coins": new_balance}})

        await update.message.reply_text(f"Successfully gave {amount} coins to user {user_id}. New balance: {new_balance}")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while giving coins. Please try again later.")



async def pay_coins(update: Update, context: CallbackContext) -> None:
    try:
        # Check if the command is a reply to a message
        if not update.message.reply_to_message:
            await update.message.reply_text("Please reply to the message of the user you want to pay.")
            return

        # Extract the recipient's user ID from the replied message
        recipient_id = int(update.message.reply_to_message.from_user.id)

        # Parse the amount from the command arguments
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Invalid format. Use: /pay <amount>")
            return

        try:
            amount = int(args[0])
        except ValueError:
            await update.message.reply_text("Invalid amount. Please provide a valid number.")
            return

        # Get the sender's user ID
        sender_id = int(update.effective_user.id)

        # Retrieve sender's and recipient's wallets
        sender_wallet = await user_collection.find_one({"id": sender_id})
        recipient_wallet = await user_collection.find_one({"id": recipient_id})

        if not sender_wallet or not recipient_wallet:
            await update.message.reply_text("Sender or recipient not found or have no wallet.")
            return

        sender_balance = sender_wallet.get("coins", 0)
        if sender_balance < amount:
            await update.message.reply_text("Insufficient balance to make the payment.")
            return

        # Update sender's balance
        new_sender_balance = sender_balance - amount
        await user_collection.update_one({"id": sender_id}, {"$set": {"coins": new_sender_balance}})

        # Update recipient's balance
        recipient_balance = recipient_wallet.get("coins", 0)
        new_recipient_balance = recipient_balance + amount
        await user_collection.update_one({"id": recipient_id}, {"$set": {"coins": new_recipient_balance}})

        await update.message.reply_text(f"Successfully transferred {amount} coins to user {recipient_id}.")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while processing the payment. Please try again later.")
      

async def show_shop(update: Update, context: CallbackContext) -> None:
    try:
        # Store the user ID in context.user_data
        context.user_data["shop_user_id"] = update.effective_user.id
        
        # Retrieve characters/items from the database
        characters_cursor = shops_collection.find()
        characters = await characters_cursor.to_list(length=None)

        if not characters:
            await update.message.reply_text("No characters found in the shop.")
            return

        # Get the current character index from context.user_data
        current_index = context.user_data.get("current_index", 0)

        # Display the current character
        character = characters[current_index]
        caption_message = f"<b>👑:</b> {character['name']}\n<b>⛩:</b> {character['anime']}\n<b>💎:</b> {character['rarity']}\n<b>💰:</b> {character['price']}\n<b>🆔:</b> {character['id']}\n<b>📌:</b> {character['about']}"
        keyboard = [
            [InlineKeyboardButton("Buy", callback_data=f"buy_{str(current_index)}")],
            [InlineKeyboardButton("Next", callback_data="next")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_photo(photo=character['img_url'], caption=caption_message, reply_markup=reply_markup, parse_mode='HTML')

        # Update the user's data to store the current index
        context.user_data["current_index"] = (current_index + 1) % len(characters)

        LOGGER.info("Character displayed in the shop.")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while displaying the shop. Please try again later.")


async def buy_character(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    
    # Check if the user is the one who initiated the shop command
    if user_id != context.user_data.get("shop_user_id"):
        await query.answer("You are not authorized to perform this action.")
        return

    try:
        # Extract character index from callback query
        character_index = int(query.data.split("_")[1])

        # Retrieve character data from the database
        characters_cursor = shops_collection.find()
        characters = await characters_cursor.to_list(length=None)

        if character_index >= len(characters):
            await query.answer("Character not found.")
            return

        character = characters[character_index]

        # Retrieve user data including wallet balance
        user = await user_collection.find_one({"id": user_id})
        if not user:
            await query.answer("User not found.")
            return

        # Check affordability
        price = character["price"]
        current_balance = user.get("coins", 0)
        if current_balance < price:
            await query.answer(f"Insufficient funds. You need {price - current_balance} more coins to buy this character.", show_alert=True)
            return

        # Deduct coins from user's wallet
        new_coins = current_balance - price

        # Add character to user's collection
        character_id = str(character["_id"])
        character_data = {
            "_id": ObjectId(),  # Generate a new ObjectId for the character entry
            "img_url": character["img_url"],
            "name": character["name"],
            "anime": character["anime"],
            "rarity": character["rarity"],
            "id": character["id"],
            "message_id": character.get("message_id")  # Optional, if message_id is available
        }

        if "characters" not in user:
            user["characters"] = []

        user["characters"].append(character_data)

        # Update user data in the database
        await user_collection.update_one(
            {"id": user_id},
            {"$set": {"coins": new_coins, "characters": user["characters"]}}
        )

        # Confirmation message
        await query.answer("Character purchased successfully.")

    except Exception as e:
        LOGGER.error(f"Error buying character: {e}")
        await query.answer("An error occurred while processing the purchase. Please try again later.", show_alert=True)


async def next_item(update: Update, context: CallbackContext) -> None:
    try:
        # Check if the user is the one who initiated the shop command
        if update.callback_query.from_user.id != context.user_data.get("shop_user_id"):
            await update.callback_query.answer("You are not authorized to perform this action.")
            return
        
        # Retrieve characters/items from the database
        characters_cursor = shops_collection.find()
        characters = await characters_cursor.to_list(length=None)

        if not characters:
            await update.callback_query.answer("No characters found in the shop.")
            return

        # Get the current character index from context.user_data
        current_index = context.user_data.get("current_index", 0)

        # Calculate the index of the next character
        next_index = (current_index + 1) % len(characters)

        # Display the next character
        character = characters[next_index]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add timestamp
        caption_message = f"👑: {character['name']}\n⛩: {character['anime']}\n💎: {character['rarity']}\n💰: {character['price']}\n🆔: {character['id']} \n📌: {character['about']}"
        keyboard = [
            [InlineKeyboardButton("Buy", callback_data=f"buy_{str(next_index)}")],
            [InlineKeyboardButton("Next", callback_data="next")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Update the user's data to store the current index
        context.user_data["current_index"] = next_index

        await update.callback_query.message.edit_media(
            media=InputMediaPhoto(media=character['img_url'], caption=caption_message),
            reply_markup=reply_markup
        )

        await update.callback_query.answer()  # Acknowledge the callback

        LOGGER.info("Next item displayed in the shop.")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.callback_query.answer("An error occurred while displaying the next item. Please try again later.")




application.add_handler(CallbackQueryHandler(next_item, pattern="^next$"))
application.add_handler(CallbackQueryHandler(buy_character, pattern=r'^buy_\d+$'))
application.add_handler(CommandHandler(['Shop', 'shopmenu'], show_shop))
application.add_handler(CommandHandler('pay', pay_coins))

# Define command handlers
REMOVE_COINS_HANDLER = CommandHandler('removecoins', remove_coins)
GIVE_COINS_HANDLER = CommandHandler('givecoins', give_coins)

# Add handlers to the application
application.add_handler(REMOVE_COINS_HANDLER)
application.add_handler(GIVE_COINS_HANDLER)

# Define command handlers
CHECK_BALANCE_HANDLER = CommandHandler('balance', check_balance)
DAILY_REWARD_HANDLER = CommandHandler('daily', daily_reward)
WEEKLY_REWARD_HANDLER = CommandHandler('weekly', weekly_reward)
TOPS_HANDLER = CommandHandler('cointop', top_users_by_coins)

# Add handlers to the application
application.add_handler(CHECK_BALANCE_HANDLER)
application.add_handler(DAILY_REWARD_HANDLER)
application.add_handler(WEEKLY_REWARD_HANDLER)
application.add_handler(TOPS_HANDLER)
