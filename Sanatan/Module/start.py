import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from Sanatan import application, VIDEO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from Sanatan import pm_users as collection 


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=GROUP_ID, 
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)})</a>", 
                                       parse_mode='HTML')
    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***Heyyyy...***

***┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/n✾ Wᴇʟᴄᴏᴍɪɴɢ ʏᴏᴜ ᴛᴏ ᴛʜᴇ Oᴛᴀᴋᴜ Cᴜʟᴛᴜʀᴇ  /n/n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/n🍂 I ᴡɪʟʟ Sᴜᴍᴍᴏɴ Rᴀɴᴅᴏᴍ Cʜᴀʀᴀᴄᴛᴇʀs/n/nIɴ ʏᴏᴜʀ Gʀᴏᴜᴘ Cʜᴀᴛ./n/n💮 Yᴏᴜ ᴄᴀɴ ᴄᴏʟʟᴇᴄᴛ ᴛʜᴇᴍ ᴀɴᴅ ᴅᴏ ᴛʀᴀᴅᴇ./n/n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/nTᴀᴘ ᴏɴ "Hᴇʟᴘ" ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
        """
        
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/Fancy_Waifu_Husbando_Bot?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/MUSIC_CHAT_GRP'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/Fancy_Waifu_Husbando_Updates')],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url=f'https://github.com/ishu9805')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        video_url = random.choice(VIDEO_URL)

        await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        video_url = random.choice(VIDEO_URL)
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/Fancy_Waifu_Husbando_Bot?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/MUSIC_CHAT_GRP'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/Fancy_Waifu_Husbando_Updates')],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url=f'https://t.me/alone_x_hater')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption="🎴Alive!?... \n connect to me in PM For more information ",reply_markup=reply_markup )

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

***┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/n✾ Wᴇʟᴄᴏᴍɪɴɢ ʏᴏᴜ ᴛᴏ ᴛʜᴇ Oᴛᴀᴋᴜ Cᴜʟᴛᴜʀᴇ  /n/n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/n🍂 I ᴡɪʟʟ Sᴜᴍᴍᴏɴ Rᴀɴᴅᴏᴍ Cʜᴀʀᴀᴄᴛᴇʀs/n/nIɴ ʏᴏᴜʀ Gʀᴏᴜᴘ Cʜᴀᴛ./n/n💮 Yᴏᴜ ᴄᴀɴ ᴄᴏʟʟᴇᴄᴛ ᴛʜᴇᴍ ᴀɴᴅ ᴅᴏ ᴛʀᴀᴅᴇ./n/n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━⧫/n/nTᴀᴘ ᴏɴ "Hᴇʟᴘ" ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
        """

        
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/MUSIC_CHAT_GRP'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/Fancy_Waifu_Husbando_Updates')],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url=f'https://github.com/ishu9805')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
