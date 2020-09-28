# -*- coding: utf-8 -*-

import logging
from xdr import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and context.
def start(update, context):
    #Send a message when the command /start is issued.
    update.message.reply_text('[!] Welcome to XDR Bot!\n\nBelow are the number of open cases:\n\n{}'.format(countWorkbench()) +'\n\nTo get more informations about how to use me type /help')
        
def help_command(update, context):
    #Send a message when the command /help is issued.
    update.message.reply_text('[!] Hello, Those are my features!!\n\n'
                              '[+] /start - Hello Message\n'
                              '[+] /help - How can you use Me\n'
                              '[+] /workbench - Open Cases\n'
                              '[+] /cases - Numbers of Open Cases\n'
                              '[+] /bdomain - Block a Domain\n'
                              '[+] /rdomain - Remove a Domain\n'
                              '[+] /roles - Roles in XDR Console\n'
                              '[+] /models - Models Available in the XDR Console\n')

def workbench(update, context):
    #Send the Workenchs opened since 09/01/2020 with High or Medium Severity.(you can edit the time queryParam variable with your desired date in xdr.py getWorkbench() function) with High or Medium Severity.
    update.message.reply_text('[+] Workbenchs:\n{}'.format(getWorkbench()))

def bdomain(update, context):
    #Send a command to XDR console to add the domain 0secops.com to the Block List. (You can setup your own domain editing the blockDomain() function in xdr.py)
    update.message.reply_text('Sending the response command...')
    action_id = blockDomain()
    status = getResponse(action_id)
    update.message.reply_text('Domain: 0secops.com\n'
                              'Response ID: {}'.format(action_id) + 
                              '\nStatus: {}'.format(status))

def rdomain(update, context):
    #Send a command to XDR console to remove the domain 0secops.com to the Block List. (You can setup your own domain editing the removeDomain() function in xdr.py)
    update.message.reply_text('Removing domain: 0secops.com ')
    update.message.reply_text('{}'.format(removeDomain()))

def roles(update, context):
    #Send a message when the command /roles is issued with all XDR possible roles.
    update.message.reply_text('[+] Found Roles:\n\n{}'.format(getRoles()))

def cases(update, context):
    #Send a message when the command /cases is issued showing the number of cases opened in the last 30 days. You can edit the countWorkbench() function in xdr.py with your desired timeframe.
    update.message.reply_text('[+] Cases opened in the last 30 days:\n\n{}'.format(countWorkbench()))

def models(update, context):
    #Send a message when the command /cases is issued showing all available machine learning models. It wasn't possible to say if the model is enable or not, because Telegram has a limitation in numbers of characteres in a message. 
    update.message.reply_text('[+] Found Models:\n{}'.format(getModels()))

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    
def unknown(update, context):
    #Send a message when the user send a message unknowm to the bot.
    update.message.reply_text('[!] Sorry, I did not understand that command. Type /help to see all available commands :)')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN_HERE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("workbench", workbench))
    dp.add_handler(CommandHandler("bdomain", bdomain))
    dp.add_handler(CommandHandler("rdomain", rdomain))
    dp.add_handler(CommandHandler("roles", roles))
    dp.add_handler(CommandHandler("models", models))
    dp.add_handler(CommandHandler("cases", cases))
     
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()



