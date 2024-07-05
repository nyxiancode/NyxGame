from telebot import TeleBot, types
from Database.database import Database
from config import OWNER_ID

def register_handlers(bot: TeleBot):
    db = Database()

    @bot.message_handler(commands=['broadcast'])
    def broadcast(message):
        if message.from_user.id != OWNER_ID:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")
            return

        msg = bot.reply_to(message, "Send the message you want to broadcast")
        bot.register_next_step_handler(msg, process_broadcast)

    def process_broadcast(message):
        users = db.get_all_users()
        for user in users:
            bot.send_message(user['_id'], message.text)
