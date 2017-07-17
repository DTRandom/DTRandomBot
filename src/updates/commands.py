import config
import json
import MySQLdb
from ..objects.user import User

def process_start_command(bot, message):
    u = User(message.sender)
    u.state("home")
    u.increaseStat('stats_command_start')

    text = (
        "<b>Benvenuto in DTRandomBot!</b>"
        "\nCon questo bot potrai <b>Parlare con me</b> o <b>Richiedere il tuo bot</b>"
        "\nPremi uno dei <b>tasti qui sotto</b> per iniziare"
    )
    bot.api.call('sendMessage', {
        'chat_id': message.chat.id, 'text': text, 'parse_mode': 'HTML', 'reply_markup':
        json.dumps(
            {'inline_keyboard': [
                [{"text": "❓ Parla con me", "callback_data": "talk"},
                 {"text": "🤖 Richiedi un bot", "callback_data": "request"}],
                [{"text": "ℹ️ Informazioni", "callback_data": "info"}]
            ]}
        )
    })
def process_admin_command(bot, message):
    if message.sender.id not in config.ADMINS:
        return

    text = (
        "🔴 <b>Benvenuto nel pannello amministratore di DTRandomBot</b>"
        "\nSeleziona un opzione:"
    )
    bot.api.call('sendMessage', {
        'chat_id': message.chat.id, 'text': text, 'parse_mode': 'HTML', 'reply_markup':
        json.dumps(
            {'inline_keyboard': [
                [{"text": "➕🌐 Nuovo post globale", "callback_data": "admin@newpost"}]
            ]}
        )
    })

def message_sent(bot, chat, message):
    u = User(message.sender)
    stato = u.state().decode('utf-8')
    if stato == "bot_talk":
        if  chat.id not in config.ADMINS:
            user_name = message.sender.id
            if message.forward_from != None:
                if message.forward_from.id == message.sender.id:
                    message.forward_to(config.ADMINS, notify = "True")
                else:
                    bot.chat(user_name).send("<i>Non sono ammessi messaggi inoltrati per motivi di sicurezza</i>", syntax = "HTML")
            else:
                message.forward_to(config.ADMINS, notify = "True")
        else:
            if message.reply_to_message is None:
                chat.send("<i>Per favore rispondi ad un messaggio per rispondere all'utente</i>", reply_to = message.message_id, syntax = "HTML")
            else:
                replyed_message = message.reply_to_message
                bot.chat(replyed_message.forward_from.id).send("<b>Admin: </b>" + message.text, syntax = 'HTML')
    else:
        return
