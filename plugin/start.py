from telebot import TeleBot, types
from Database.database import Database

def register_handlers(bot: TeleBot):
    db = Database()

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        db.initialize_user(message.from_user.id, message.from_user.username)
        bot.send_message(message.chat.id, "Welcome to the Farm Game!")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.send_message(message.chat.id, "Use /reg to register, /top to see top players, /cost for prices, /buy to buy animals, /myinfo for your info, /sell to sell products.")
