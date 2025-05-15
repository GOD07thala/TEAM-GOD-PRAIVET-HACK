
import telebot
import time
import json
from datetime import datetime, timedelta

BOT_TOKEN = '7945482985:AAFtERvKYVvFh1TaPV21yo7nTAoMk6vmy1g'
ADMIN_ID = 6722166633  # Replace with your Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)
keys = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Welcome Admin!\nSend `/createkey <minutes>` to generate a key.")
    else:
        bot.send_message(message.chat.id, "Access Denied")

@bot.message_handler(commands=['createkey'])
def create_key(message):
    if message.chat.id != ADMIN_ID:
        return
    try:
        _, minutes = message.text.split()
        expiry = datetime.now() + timedelta(minutes=int(minutes))
        key = f"KEY{int(time.time())}"
        keys[key] = expiry.strftime('%Y-%m-%d %H:%M:%S')
        save_keys()
        bot.send_message(message.chat.id, f"✅ Key: `{key}`\n⏳ Expires: {keys[key]}", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "❌ Invalid command. Use /createkey <minutes>")

def save_keys():
    with open('keys.json', 'w') as f:
        json.dump(keys, f)

def load_keys():
    global keys
    try:
        with open('keys.json', 'r') as f:
            keys = json.load(f)
    except:
        keys = {}

load_keys()
bot.polling()
