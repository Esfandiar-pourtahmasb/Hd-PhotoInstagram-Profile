#instabot
from instagramy import InstagramUser
import requests
from telegram.ext.filters import Filters
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler
    )

from datetime import date

users_log = {}

def start(update, context):
    msg = """Send Instagram Username with /users command. example:\n/users user1 user2 ... user5\nin single day you can enter 30 user.\n
    you can reset with /reset command"""
    context.bot.send_message(update.effective_message.chat_id, msg)


def send_hd_photo(update, context):

    if len(context.args) > 5:
        try:
            context.bot.send_message(update.effective_message.chat_id, 'too many usernames. exceeded from 5')
        except BaseException as e:
            print('Error type is: ', type(e))
            #print(e.message)
        return
    if len(context.args) == 0:
        try:
            context.bot.send_message(update.effective_message.chat_id, 'pls enter username like\n /users user1 user2 ...')
        except BaseException as e:
            print('Error type is: ', type(e))
            #print(e.message)
        return

    print(update.effective_user.first_name, ': ', end = ' ')
    print(context.args)
    
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    
    users_log.setdefault(update.effective_user.id, [0, today])
    if users_log[update.effective_user.id][0] >= 30:
        msg = 'dear {0}, today you have sent over than 30 usernames on this bot\npls try /reset command or try another day'.format(update.effective_user.first_name)
        try:
            context.bot.send_message(update.effective_message.chat_id, msg)
        except BaseException as e:
            print(type(e))
            #print(e.message)
        return

    for user in context.args:
        try:
            user = InstagramUser(user, sessionid="sessionid")
            link = user.user_data['profile_pic_url_hd']
            context.bot.send_photo(update.effective_message.chat_id, link)
        except BaseException as e:
            print(type(e))
            #print(e.message)
        users_log[update.effective_user.id][0]+= 1

def reset(update, context):
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    if users_log.get(update.effective_user.id, -1) == -1:
        try:
            context.bot.send_message(update.effective_message.chat_id, 'successful reset')
        except BaseException as e:
            print(type(e))
            #print(e.message)
    else:
        if today != users_log[update.effective_user.id][1]:
            try:
                users_log[update.effective_user.id][1] = today
                users_log[update.effective_user.id][0] = 0
                context.bot.send_message(update.effective_message.chat_id, 'successful reset')
            except BaseException as e:
                print(type(e))
                #print(e.message)
        else:
            try:
                context.bot.send_message(update.effective_message.chat_id, 'you can\'t reset today. try another day')
            except BaseException as e:
                print(type(e))
                #print(e.message)

def unknown(update, context):
    try:
        msg = 'unknown command\n try /start or /reset or /users command'
        context.bot.send_message(update.effective_message.chat_id, msg)
    except BaseException as e:
        print(type(e))
        #print(e.message)

up = Updater(token = 'Token')

up.dispatcher.add_handler(CommandHandler('start', start))
up.dispatcher.add_handler(CommandHandler('users', send_hd_photo))
up.dispatcher.add_handler(CommandHandler('reset', reset))
up.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
#up.dispatcher.add_handler(MessageHandler(Filters.update, unknown))
up.start_polling()
up.idle()

