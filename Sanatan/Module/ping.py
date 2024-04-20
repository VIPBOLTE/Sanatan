import random
import time
import psutil
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


from Sanatan import application, sudo_users
# Define a list of image URLs
image_urls = [
    "https://telegra.ph/file/81df55fc1b39927769239.jpg",
    "https://telegra.ph/file/5ed3faf822c1b8a4d1d02.jpg",
    # Add more image URLs as needed
]

async def ping(update: Update, context: CallbackContext) -> None:
    # Check if the user is authorized to use the command
    if str(update.effective_user.id) not in sudo_users:
        update.message.reply_text("Nouu.. its Sudo user's Command..")
        return

    # Select a random image URL
    random_image = random.choice(image_urls)

    # Response Time
    start_time = time.time()
    message = await update.message.reply_text('Pong!')
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    
    # Uptime
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_hours = uptime_seconds / 3600

    # RAM Usage
    ram_usage = psutil.virtual_memory().percent

    # CPU Usage
    cpu_usage = psutil.cpu_percent()

    # Disk Usage
    disk_usage = psutil.disk_usage('/').percent

    # Ping response with random image
    ping_response = f'Pong! {elapsed_time}ms\n\n'
    ping_response += f'Uptime: {uptime_hours:.2f} hours\n'
    ping_response += f'RAM Usage: {ram_usage}%\n'
    ping_response += f'CPU Usage: {cpu_usage}%\n'
    ping_response += f'Disk Usage: {disk_usage}%'

    # Send the ping response along with the random image
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=random_image, caption=ping_response)

# Add the CommandHandler to the dispatcher
application.add_handler(CommandHandler("ping", ping))
