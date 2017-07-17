import json
import os
from datetime import datetime, timedelta
import config
from botogram.api import APIError

def process_callback(bot, cb, u):

    if cb.query == "home":
        text = (
            "<b>Benvenuto in DTRandomBot!</b>"
            "\nCon questo bot potrai <b>Parlare con me</b> o <b>Richiedere il tuo bot</b>"
            "\nPremi uno dei <b>tasti qui sotto</b> per iniziare"
        )
        bot.api.call('sendMessage', {
            'chat_id': cb.chat.id, 'text': text, 'parse_mode': 'HTML', 'reply_markup':
            json.dumps(
                {'inline_keyboard': [
                    [{"text": "❓ Parla con me", "callback_data": "talk"},
                     {"text": "🤖 Richiedi un bot", "callback_data": "request"}],
                    [{"text": "ℹ️ Informazioni", "callback_data": "info"}]
                ]}
            )
        })
        cb.notify("🏡 Menù principale")

    elif cb.query == "info":
        u.state("info")
        text = (
            "<b>Informazioni sul bot</b>"
            "\n<i>Link utili</i>"
            "\n➖ Entra nel <b>📢 Canale ufficiale</b> per ricevere <b>news</b> e <b>aggiornamenti</b> "
            "in anteprima <b>sul bot</b>"
            "\n➖ <b>💰 Dona</b> <i>quello che vuoi</i> per tenere <b>il bot online</b> e per supportare "
            "<b>il lavoro dello sviluppatore</b>"
            "\n➖ Dai un'occhiata o contribuisci al <i>codice sorgente</i> su <b>🔘 GitHub</b>"
            "\n➖ Visualizza le <b>📈 Statistiche</b> di utilizzo del bot!"
        )
        bot.api.call("editMessageText", {
            "chat_id": cb.chat.id, "message_id": cb.message.message_id, "text": text,
            "parse_mode": "HTML", "reply_markup":
            json.dumps(
                {'inline_keyboard': [
                    [{"text": "📢 Canale ufficiale", "url": "https://t.me/DTRandomChannel"}],
                    [{"text": "💰 Dona", "url": "https://paypal.me/FZimbolo/1"},
                     {"text": "🔘 GitHub", "url": "https://google.com"}],
                    [{"text": "⬅️ Torna indietro", "callback_data": "home"}]
                ]}
            )
        })
        cb.notify("ℹ️ Altre informazioni")

    elif cb.query == "talk":
        u.state("talk")
        text = (
            "<b>❓ Parla con me</b>"
            "\n<b>Scrivi</b> a <b>questo bot</b> o al mio <b>profilo privato</b> "
            "per dare un suggerimento o fare una domanda"
            "\n\nScegli un'opzione:"
        )
        bot.api.call("editMessageText", {
            "chat_id": cb.chat.id, "message_id": cb.message.message_id, "text": text,
            "parse_mode": "HTML", "reply_markup":
            json.dumps(
                {"inline_keyboard": [
                    [{"text": "👤Contattami", "callback_data": "bot_talk"},
                     {"text": "Profilo privato", "url": "https://t.me/DTRandom"}],
                    [{"text": "⬅️ Torna indietro", "callback_data": "home"}]
                ]}
            )
        })
        cb.notify("❓ Parla con me")

    elif cb.query == "bot_talk":
        u.state("bot_talk")
        text = (
            "<b>👤 Contattami</b>"
            "\n<b>Scrivi a questo bot</b>, io lo riceverò e ti risponderò appena possibile"
        )
        bot.api.call("editMessageText", {
            "chat_id": cb.chat.id, "message_id": cb.message.message_id, "text": text,
            "parse_mode": "HTML", "reply_markup":
            json.dumps(
                {"inline_keyboard": [
                    [{"text": "⬅️ Torna Indietro", "callback_data": "talk"}]
                ]}
            )
        })
        cb.notify("👤 Contattami")
