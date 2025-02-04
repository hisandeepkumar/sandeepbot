import importlib
import re
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.constants import ParseMode
from telegram import TelegramError
from telegram._exceptions import BadRequest, TimedOut, NetworkError, ChatMigrated, Unauthorized
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown

# ======= ADD YOUR BOT TOKEN & OWNER ID HERE =======
TOKEN = "7941135502:AAHz-KGvAAoZEhPVgfVKw3zFbkaB0_Pi5rM"  # Your bot's API token
OWNER_ID = 878604830  # Your Telegram User ID
# ==============================================

from tg_bot import dispatcher, updater, WEBHOOK, DONATION_LINK, CERT_PATH, PORT, URL, LOGGER, ALLOW_EXCL
from tg_bot.modules import ALL_MODULES
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.misc import paginate_modules

# ======== BOT START MESSAGE ==========
PM_START_TEXT = """
welcome.
"""
# ======================================

# HELP MESSAGE STRING
HELP_STRINGS = """
Hey there! My name is *{}*.
I'm a modular group management bot with a few fun extras! Have a look at the following for an idea of some of \
the things I can help you with.
*Main* commands available:
 - /start: start the bot
 - /help: PM's you this message.
 - /help <module name>: PM's you info about that module.

 - /settings:
   - in PM: will send you your settings for all supported modules.
   - in a group: will redirect you to pm, with all that chat's settings.
{}
""".format(dispatcher.bot.first_name, "" if not ALLOW_EXCL else "\nAll commands can either be used with / or !.\n")

# COMMAND TO START THE BOT
@run_async
def start(bot: Bot, update: Update, args: List[str]):
    if update.effective_chat.type == "private":
        first_name = update.effective_user.first_name
        update.effective_message.reply_text(
            PM_START_TEXT.format(escape_markdown(first_name), escape_markdown(bot.first_name), OWNER_ID),
            parse_mode=ParseMode.MARKDOWN, 
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="🎉 Add me to your group", url="t.me/{}?startgroup=true".format(bot.username)),  
                     InlineKeyboardButton(text="🤖 Make Own Admin Bot", url="")],
                    [InlineKeyboardButton(text="👥 Support Group", url=""), 
                     InlineKeyboardButton(text="🔔 Update Channel", url="")],
                    [InlineKeyboardButton(text="👨‍💻 Make", url=""), 
                     InlineKeyboardButton(text="🛠 Help", url="https://t.me/{}?start=help".format(bot.username)) ]
                ]
            )
        )

# HANDLE HELP COMMAND
@run_async
def get_help(bot: Bot, update: Update):
    chat = update.effective_chat  
    args = update.effective_message.text.split(None, 1)

    if chat.type != chat.PRIVATE:
        update.effective_message.reply_text("Contact me in PM to get the list of possible commands.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           bot.username))]]))
        return
    else:
        send_help(chat.id, HELP_STRINGS)

# FUNCTION TO SEND SETTINGS
def send_settings(chat_id, user_id, user=False):
    if user:
        dispatcher.bot.send_message(user_id, "These are your current settings.", parse_mode=ParseMode.MARKDOWN)
    else:
        dispatcher.bot.send_message(user_id, "Chat settings are available!", parse_mode=ParseMode.MARKDOWN)

# COMMAND TO GET SETTINGS
@run_async
def get_settings(bot: Bot, update: Update):
    chat = update.effective_chat  
    user = update.effective_user  
    msg = update.effective_message  

    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            msg.reply_text("Click here to get this chat's settings.",
                           reply_markup=InlineKeyboardMarkup(
                               [[InlineKeyboardButton(text="Settings",
                                                      url="t.me/{}?start=stngs_{}".format(
                                                          bot.username, chat.id))]]))
    else:
        send_settings(chat.id, user.id, True)

# MAIN FUNCTION TO START THE BOT
def main():
    start_handler = CommandHandler("start", start, pass_args=True)
    help_handler = CommandHandler("help", get_help)
    settings_handler = CommandHandler("settings", get_settings)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)
    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    updater.idle()

if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
