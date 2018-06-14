from Tag import *
import config
# import validators as vl
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = config.token
admin_id = 189766950
updater = Updater(token = token)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="""
    Hello!
    This is a Tags Bot. It to service @lifeONet channel.
    Usage:
    /start or /help - this text
    /tags - view list all tags
    """)

def tags(bot, update):
    cursor = Tag.showAll()
    res = ""
    for doc in cursor:
        res += doc["name"] + " "


    # print(res)            
    bot.send_message(chat_id=update.message.chat_id, text=res)
    
                            
def isAdmin(fn):
    
    def admin(bot, update):
        chat_id = update.message.chat_id
        if chat_id == admin_id:
            fn(bot, update)
        else:
            bot.send_message(chat_id, text="ACCESS DENIED")
    return admin

def tag(bot, update):
    prep_query = re.findall('#\w+', update.message.text)
    if not prep_query:
        info = """
        Usage: /tag <tagName>
        """
        bot.send_message(chat_id=update.message.chat_id, text=info)
    else:
        t = Tag(prep_query[0])
        urls = t.show()
        bot.send_message(chat_id=update.message.chat_id, text=urls)

@isAdmin
def test(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="bla bla")

@isAdmin    
def tagUpdate(bot, update):
    chat_id = update.message.chat_id
    # if isAdmin(chat_id):
    msg_text = update.message.text
    prep_query = re.findall('(#\w+)\s(https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),])+)', msg_text)

    if not prep_query :
        
        info = """
        Update tag info or added tag into DB.
        Usage: /tagupdate #nameTag http://link.to/post?or=another&url=1
        """
        
        bot.send_message(chat_id, text=info)
    else:
        tag = prep_query[0][0]
        url = prep_query[0][1]
            # TODO: save to DB
        t = Tag(tag, url)
        print(tag)
        st = t.save()
        bot.send_message(chat_id, text=st)

    # else:
    #     bot.send_message(chat_id, text="ACCESS DENIED")


tag_handler = CommandHandler('tag', tag)
start_handler = CommandHandler(['start', 'help'], start)
tagUpdate_handler = CommandHandler('tagupdate', tagUpdate)
test_handler = CommandHandler('test', test)
tags_handler = CommandHandler('tags', tags)
dispatcher.add_handler(tag_handler)
dispatcher.add_handler(tags_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(tagUpdate_handler)
dispatcher.add_handler(test_handler)

# dispatcher.add_handler(MessageHandler(Filters.text, echo, channel_post_updates = True))

updater.start_polling()

