from .. import main


class Callback:
    """
    Callback base object
    """
    def __init__(self, update):
        """
        Create a callback object
        :param update: Telegram's update object
        """
        self.update = update.callback_query
        self.id = self.update.id
        self.query = self.update.data
        self.sender = self.update.sender
        self.message = self.update.message
        self._api = main.bot.api

        self.isInline = (True if not self.message else False)
        self.inline_message_id = (self.update.inline_message_id if self.isInline else None)
        self.chat = (self.message.chat if not self.isInline else None)

    def notify(self, text, alert=False, cache_time=0):
        self._api.call("answerCallbackQuery", {
            "callback_query_id": self.id,
            "text": text,
            "show_alert": alert,
            "cache_time": cache_time
        })
