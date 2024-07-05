from telebot import TeleBot
from config import CHANNEL_ID

def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=['start', 'reg', 'buy', 'sell'])
    def log_to_channel(message):
        log_message = f"User {message.from_user.username} used command {message.text}"
        bot.send_message(CHANNEL_ID, log_message)
        bot.process_new_messages([message])
