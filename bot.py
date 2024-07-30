import os
import re
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
TARGET_CHAT_ID = os.getenv('TARGET_CHAT_ID')
NEW_LINK = os.getenv('NEW_LINK')

bot = Bot(TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am a forwarder bot.')

def replace_links(text, new_link):
    return re.sub(r'http\S+', new_link, text)

def forward_message(update: Update, context: CallbackContext) -> None:
    message = update.message
    if message.text:
        new_text = replace_links(message.text, NEW_LINK)
        bot.send_message(chat_id=TARGET_CHAT_ID, text=new_text)
    elif message.photo:
        caption = replace_links(message.caption, NEW_LINK) if message.caption else None
        bot.send_photo(chat_id=TARGET_CHAT_ID, photo=message.photo[-1].file_id, caption=caption)
    elif message.video:
        caption = replace_links(message.caption, NEW_LINK) if message.caption else None
        bot.send_video(chat_id=TARGET_CHAT_ID, video=message.video.file_id, caption=caption)
    elif message.document:
        caption = replace_links(message.caption, NEW_LINK) if message.caption else None
        bot.send_document(chat_id=TARGET_CHAT_ID, document=message.document.file_id, caption=caption)
    elif message.sticker:
        bot.send_sticker(chat_id=TARGET_CHAT_ID, sticker=message.sticker.file_id)

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, forward_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()