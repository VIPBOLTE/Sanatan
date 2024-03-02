from telegram import Update
from harem import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define your Telegram Bot API token here
TOKEN = "your_telegram_bot_token_here"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send /pp followed by an image to get its details!')

def image_details(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo_file_id = update.message.reply_to_message.photo[-1].file_id
        photo_url = context.bot.get_file(photo_file_id).file_path
        details_link = f"https://example.com/get_image_details?url={photo_url}"
        update.message.reply_text(f"Details for the image: {details_link}")
    else:
        update.message.reply_text("Please reply to an image to get its details.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pp", image_details))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

