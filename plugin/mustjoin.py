from telebot import TeleBot, types
from config import CHANNEL_ID

def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=['start', 'help', 'reg', 'buy', 'sell', 'myinfo'])
    def check_membership(message):
        user_status = bot.get_chat_member(CHANNEL_ID, message.from_user.id).status
        if user_status not in ['member', 'administrator', 'creator']:
            markup = types.InlineKeyboardMarkup()
            join_button = types.InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_ID}")
            markup.add(join_button)
            bot.send_message(message.chat.id, "You must join the channel to use this bot", reply_markup=markup)
        else:
            bot.process_new_messages([message])
