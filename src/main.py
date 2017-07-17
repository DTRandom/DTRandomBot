import botogram
import botogram.objects.base

import config
from .objects.callback import Callback
from .objects.user import User
from .updates import commands, callback

class CallbackQuery(botogram.objects.base.BaseObject):
    def __init__(self, update):
        super().__init__(update)

    required = {
        "id": str,
        "from": botogram.User,
        "data": str,
    }
    optional = {
        "inline_message_id": str,
        "message": botogram.Message,
    }
    replace_keys = {
        "from": "sender"
    }

class InlineQuery(botogram.objects.base.BaseObject):
    def __init__(self, update):
        super().__init__(update)

    required = {
        "id": str,
        "from": botogram.User,
        "query": str,
        "offset": str,
    }
    optional = {
        "location": botogram.Location,
    }
    replace_keys = {
        "from": "sender"
    }

botogram.Update.optional["callback_query"] = CallbackQuery
botogram.Update.optional["inline_query"] = InlineQuery

bot = botogram.create(config.BOT_TOKEN)
@bot.process_message
def limitatibot(chat, message):
    commands.message_sent(bot, chat, message)
    

@bot.command("start")
def start(message, args):
    """Avvia il bot"""
    if args:
        deeplinking.process_deeplinking(bot, message, args)
        return

    commands.process_start_command(bot, message)
@bot.command("admin", hidden=True)
def admin(message):
    commands.process_admin_command(bot, message)

def process_callback(__bot, __chains, update):
    del (__bot, __chains)  # Useless arguments from botogram
    cb = Callback(update)
    u = User(cb.sender)
    u.increaseStat('stats_callback_count')

    callback.process_callback(bot, cb, u)

bot.register_update_processor("callback_query", process_callback)
