import os
import telebot


class TelegramHelper:
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, text):
        try:
            self.bot.send_message(
                chat_id=self.chat_id, text=text, parse_mode="markdown"
            )
        except telebot.apihelper.ApiException as e:
            print(f"Error sending message to Telegram: {e}")


telegram_helper = TelegramHelper()
