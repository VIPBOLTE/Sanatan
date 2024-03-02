from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from Sanatan import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT
 

 

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send /pp followed by an image to get its details!')

async def image_details(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message.photo:
     photo_file_id = update.message.reply_to_message.photo[-1].file_id
     photo_url = context.bot.get_file(photo_file_id).file_path
     details_link = f"https://google.com/get_image_details?url={photo_url}"
     await update.message.reply_text(f"Details for the image: {details_link}")
    else:
     await update.message.reply_text("Please reply to an image to get its details.")



image_detail = CallbackHandler('pp', image_details, block=False)
application.add_handler(image_detail)

