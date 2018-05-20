import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = config.token

updater = Updater(token = token)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm a LIVE!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
# dispatcher.add_handler(MessageHandler(Filters.text, echo, channel_post_updates = True))

updater.start_polling()

