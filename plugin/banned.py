from telebot import TeleBot
from Database.database import Database
from config import OWNER_ID

def register_handlers(bot: TeleBot):
    db = Database()

    @bot.message_handler(commands=['ban'])
    def ban_user(message):
        if message.from_user.id != OWNER_ID:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")
            return

        msg = bot.reply_to(message, "Send the user ID to ban")
        bot.register_next_step_handler(msg, process_ban)

    def process_ban(message):
        user_id = int(message.text)
        db.ban_user(user_id)
        bot.send_message(message.chat.id, f"User {user_id} has been banned.")

    @bot.message_handler(commands=['unban'])
    def unban_user(message):
        if message.from_user.id != OWNER_ID:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")
            return

        msg = bot.reply_to(message, "Send the user ID to unban")
        bot.register_next_step_handler(msg, process_unban)

    def process_unban(message):
        user_id = int(message.text)
        db.unban_user(user_id)
        bot.send_message(message.chat.id, f"User {user_id} has been unbanned.")
