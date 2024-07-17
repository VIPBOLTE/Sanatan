import urllib.request
from pymongo import ReturnDocument
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from Sanatan import application collection, db
from config import LOGGER_ID, SUPPORT_CHAT, OWNER_USERNAME, sudo_users

WRONG_FORMAT_TEXT = """
Wʀᴏɴɢ ❌ ғᴏʀᴍᴀᴛ...  ᴇɢ. /hupload Iᴍɢ_ᴜʀʟ ᴍᴜᴢᴀɴ-ᴋɪʙᴜᴛsᴜɪɪ Dᴇᴍᴏɴ-sʟᴀʏᴇʀ 3

ɪᴍɢ_ᴜʀʟ ᴄʜᴀʀᴀᴄᴛᴇʀ-ɴᴀᴍᴇ ᴀɴɪᴍᴇ-ɴᴀᴍᴇ ʀᴀʀɪᴛʏ-ɴᴜᴍʙᴇʀ

ᴜsᴇ ʀᴀʀɪᴛʏ ɴᴜᴍʙᴇʀ ᴀᴄᴄᴏʀᴅɪɴɢʟʏ ʀᴀʀɪᴛʏ Mᴀᴘ

🏆ʀᴀʀɪᴛʏ_ᴍᴀᴘ
1: 🟢 Cᴏᴍᴍᴏɴ
2: 🟣 Rᴀʀᴇ
3: 🟡 Lᴇɢᴇɴᴅᴀʀʏ
4: 🔮 Lɪᴍɪᴛᴇᴅ
5: 🫧 Pʀᴇᴍɪᴜᴍ
"""

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

async def hupload(update: Update, context: CallbackContext) -> None:
    try:
        if update.effective_chat.type == "private":
            await update.message.reply_text(
                "Please use this command in the group chat.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Support Chat", url=f"https://t.me/{SUPPORT_CHAT}")]
                ])
            )
            return

        args = context.args
        if len(args) != 4:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        try:
            urllib.request.urlopen(args[0])
        except:
            await update.message.reply_text('Invalid URL.')
            return

        rarity_map = {
            1: "🟢 Cᴏᴍᴍᴏɴ", 
            2: "🟣 Rᴀʀᴇ", 
            3: "🟡 Lᴇɢᴇɴᴅᴀʀʏ", 
            4: "🔮 Lɪᴍɪᴛᴇᴅ", 
            5: "🫧 Pʀᴇᴍɪᴜᴍ"
        }
        try:
            rarity = rarity_map[int(args[3])]
        except KeyError:
            await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, or 5.')
            return

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id,
            'uploaded_by': update.effective_user.first_name
        }

        await update.message.reply_text(f'@{OWNER_USERNAME} Please wait for approval.', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Approve", callback_data=f"upload_yes_{id}"), InlineKeyboardButton("Reject", callback_data=f"upload_no_{id}")]
        ]))
        context.chat_data['character_pending_approval'] = character
        
    except Exception as e:
        await update.message.reply_text(f'Character Upload Unsuccessful. Error: {str(e)}\nIf you think this is a source error, forward to: https://t.me/{SUPPORT_CHAT}')

async def upload_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    callback_data = query.data.split('_')
    action = callback_data[1]
    character_id = callback_data[2]

    if action == 'yes' and str(user_id) in sudo_users:
        await query.answer()
        # Fetch character details
        character = context.chat_data.get('character_pending_approval')
        if character and character['id'] == character_id:
            character_name = character['name']
            anime_name = character['anime']
            rarity = character['rarity']
            uploaded_by = character['uploaded_by']
            message_text = f"<b>img_url</b>: {character['img_url']}\n" \
                           f"<b>Character name</b>: {character_name}\n" \
                           f"<b>Anime name</b>: {anime_name}\n" \
                           f"<b>Rarity</b>: {rarity}\n" \
                           f"<b>ID</b>: {character_id}\n" \
                           f"Uploaded by: {uploaded_by}"
            await query.message.reply_photo(character['img_url'], caption=message_text, parse_mode='HTML')
            await collection.insert_one(character)  # Store character in the collection
            del context.chat_data['character_pending_approval']  # Remove character from pending approval
        else:
            await query.message.reply_text("Character details not found or mismatch.")
        await query.message.delete()
    elif action == 'no' and str(user_id) in sudo_users:
        await query.answer()
        await query.message.reply_text('Your character is not approved.')
        del context.chat_data['character_pending_approval']  # Remove character from pending approval
        await query.message.delete()

HUPLOAD_HANDLER = CommandHandler('hupload', hupload, block=False)
application.add_handler(HUPLOAD_HANDLER)
UPLOAD_CALLBACK_HANDLER = CallbackQueryHandler(upload_callback, pattern='^upload_(yes|no)_')
application.add_handler(UPLOAD_CALLBACK_HANDLER)
