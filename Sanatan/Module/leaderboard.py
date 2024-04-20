import os
import random
import html

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from Sanatan import (application,
                    user_collection, top_global_groups_collection, top_global_groups_collection, 
                    group_user_totals_collection)
from config import OWNER_ID
from Sanatan import sudo_users as SUDO_USERS 
LEADERBOARD_URL = [ 
             "https://telegra.ph/file/5ed3faf822c1b8a4d1d02.jpg", 
             "https://telegra.ph/file/81df55fc1b39927769239.jpg", 
           ]
async def global_leaderboard(update: Update, context: CallbackContext) -> None:
    
    cursor = top_global_groups_collection.aggregate([
        {"$project": {"group_name": 1, "count": 1}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>TOP 10 GROUPS WHO GUESSED MOST CHARACTERS</b>\n\n"

    for i, group in enumerate(leaderboard_data, start=1):
        group_name = html.escape(group.get('group_name', 'Unknown'))

        if len(group_name) > 10:
            group_name = group_name[:15] + '...'
        count = group['count']
        leaderboard_message += f'{i}. <b>{group_name}</b> ➾ <b>{count}</b>\n'
    
    
    photo_url = random.choice(LEADERBOARD_URL)

    await update.message.reply_video(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def ctop(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    cursor = group_user_totals_collection.aggregate([
        {"$match": {"group_id": chat_id}},
        {"$project": {"username": 1, "first_name": 1, "character_count": "$count"}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>TOP 10 USERS WHO GUESSED CHARACTERS MOST TIME IN THIS GROUP..</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
    
    photo_url = random.choice(LEADERBOARD_URL)

    await update.message.reply_video(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')


async def leaderboard(update: Update, context: CallbackContext) -> None:
    # Fetch all users with their character counts
    cursor = user_collection.find({}, {"_id": 0, "username": 1, "first_name": 1, "characters": 1})

    # Convert cursor to list
    leaderboard_data = await cursor.to_list(length=None)

    # Sort the list based on character count
    leaderboard_data.sort(key=lambda x: len(x.get('characters', [])), reverse=True)

    # Limit to top 10 users
    leaderboard_data = leaderboard_data[:10]

    # Prepare the leaderboard message
    leaderboard_message = "<b>TOP 10 USERS WITH MOST CHARACTERS</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = len(user.get('characters', []))  # Calculate character count
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
    
    photo_url = random.choice(LEADERBOARD_URL)

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')




async def stats(update: Update, context: CallbackContext) -> None:
    
    user_count = await user_collection.count_documents({})


    group_count = await group_user_totals_collection.distinct('group_id')


    await update.message.reply_text(f'Total Users: {user_count}\nTotal groups: {len(group_count)}')




async def send_users_document(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('only For Sudo users...')
        return
    cursor = user_collection.find({})
    users = []
    async for document in cursor:
        users.append(document)
    user_list = ""
    for user in users:
        user_list += f"{user['first_name']}\n"
    with open('users.txt', 'w') as f:
        f.write(user_list)
    with open('users.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('users.txt')

async def send_groups_document(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('Only For Sudo users...')
        return
    cursor = top_global_groups_collection.find({})
    groups = []
    async for document in cursor:
        groups.append(document)
    group_list = ""
    for group in groups:
        group_list += f"{group['group_name']}\n"
        group_list += "\n"
    with open('groups.txt', 'w') as f:
        f.write(group_list)
    with open('groups.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('groups.txt')


application.add_handler(CommandHandler('ctop', ctop, block=False))
application.add_handler(CommandHandler('stats', stats, block=False))
application.add_handler(CommandHandler('TopGroups', global_leaderboard, block=False))

application.add_handler(CommandHandler('list', send_users_document, block=False))
application.add_handler(CommandHandler('groups', send_groups_document, block=False))


application.add_handler(CommandHandler('top', leaderboard, block=False))
