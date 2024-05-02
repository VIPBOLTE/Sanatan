import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from Sanatan import application, db
from Sanatan import pm_users as collection 
from config import SUPPORT_CHAT, SUPPORT_CHANNEL, BOT_USERNAME, LOGGER_ID, OWNER_USERNAME


IMG_URL = [
"https://telegra.ph/file/3134ed3b57eb051b8c363.jpg",
"https://telegra.ph/file/5a2cbb9deb62ba4b122e4.jpg",
"https://telegra.ph/file/cb09d52a9555883eb0f61.jpg"

]



async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=LOGGER_ID, 
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)})</a>", 
                                       parse_mode='HTML')
    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***Heyyyy...***

***┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***✾ Wᴇʟᴄᴏᴍɪɴɢ ʏᴏᴜ ᴛᴏ ᴛʜᴇ Oᴛᴀᴋᴜ Cᴜʟᴛᴜʀᴇ***
***┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***🍂 I ᴡɪʟʟ Sᴜᴍᴍᴏɴ Rᴀɴᴅᴏᴍ Cʜᴀʀᴀᴄᴛᴇʀs***
***Iɴ ʏᴏᴜʀ Gʀᴏᴜᴘ Cʜᴀᴛ.***
***💮 Yᴏᴜ ᴄᴀɴ ᴄᴏʟʟᴇᴄᴛ ᴛʜᴇᴍ ᴀɴᴅ ᴅᴏ ᴛʀᴀᴅᴇ.***
***┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***Tᴀᴘ ᴏɴ "Hᴇʟᴘ" ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
        """
        
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{SUPPORT_CHANNEL}')],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url=f'https://t.me/{OWNER_USERNAME}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(IMG_URL)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(IMG_URL)
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{SUPPORT_CHANNEL}')],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url=f'https://t.me/{OWNER_USERNAME}')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="🎴Alive!?... \n connect to me in PM For more information ",reply_markup=reply_markup )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***Help Section:***
    
***/guess: To Guess character (only works in group)***
***/fav: Add Your fav***
***/trade : To trade Characters***
***/gift: Give any Character from Your Collection to another user.. (only works in groups)***
***/collection: To see Your Collection***
***/topgroups : See Top Groups.. Ppl Guesses Most in that Groups***
***/top: Too See Top Users***
***/ctop : Your ChatTop***
***/changetime: Change Character appear time (only works in Groups)***
   """
        help_keyboard = [[InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***Hoyyyy...*** ✨

***┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***✾ Wᴇʟᴄᴏᴍɪɴɢ ʏᴏᴜ ᴛᴏ ᴛʜᴇ Oᴛᴀᴋᴜ Cᴜʟᴛᴜʀᴇ***
***┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***🍂 I ᴡɪʟʟ Sᴜᴍᴍᴏɴ Rᴀɴᴅᴏᴍ Cʜᴀʀᴀᴄᴛᴇʀs***
***Iɴ ʏᴏᴜʀ Gʀᴏᴜᴘ Cʜᴀᴛ.***
***💮 Yᴏᴜ ᴄᴀɴ ᴄᴏʟʟᴇᴄᴛ ᴛʜᴇᴍ ᴀɴᴅ ᴅᴏ ᴛʀᴀᴅᴇ.***
***┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫***
***Tᴀᴘ ᴏɴ "Hᴇʟᴘ" ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
        """

        
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{SUPPORT_CHANNEL}')],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url=f'https://t.me/{OWNER_USERNAME}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
