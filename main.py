from telebot import TeleBot
from config import TOKEN
from plugin import start, farm, broadcast, mustjoin, banned, logchannel

bot = TeleBot(TOKEN)

# Register handlers from plugins
start.register_handlers(bot)
farm.register_handlers(bot)
broadcast.register_handlers(bot)
mustjoin.register_handlers(bot)
banned.register_handlers(bot)
logchannel.register_handlers(bot)

if __name__ == "__main__":
    bot.polling(none_stop=True)
