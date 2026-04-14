from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import logging
import json
from datetime import datetime
import os

# ====== CONFIG ======
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@taj7onway"

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)

# ====== DATABASE FILE ======
DB_FILE = "users.json"

def load_users():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ====== START COMMAND ======
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    users = load_users()

    user_id = str(user.id)

    if user_id not in users:
        users[user_id] = {
            "name": user.first_name,
            "joined_at": str(datetime.now()),
            "active": True
        }
        save_users(users)

    keyboard = [
        [InlineKeyboardButton("🚀 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://img.freepik.com/premium-vector/stylish-welcome-lettering-modern-banner-design_1188421-3705.jpg"

    caption = f"""
🔥 *WELCOME {user.first_name}* 🔥

💰 Daily Premium Content
📈 High Profit Updates
🎯 Limited Access

👇 Join Now & Start With Us 👇
"""

    update.message.reply_photo(
        photo=image_url,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ====== MESSAGE TRACKING ======
def track_messages(update: Update, context: CallbackContext):
    user = update.effective_user
    users = load_users()

    user_id = str(user.id)

    if user_id in users:
        users[user_id]["last_active"] = str(datetime.now())
        save_users(users)

# ====== MAIN ======
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, track_messages))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, start))
    dp.add_handler(MessageHandler(Filters.all, track_messages))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
