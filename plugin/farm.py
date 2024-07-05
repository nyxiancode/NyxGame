from telebot import TeleBot, types
from Database.database import Database
from random import randint

def register_handlers(bot: TeleBot):
    db = Database()


    @bot.message_handler(commands=['reg'])
    def register_user(message):
        db.initialize_user(message.from_user.id, message.from_user.username)
        db.add_nyx_coin(message.from_user.id, 50)
        bot.send_message(message.chat.id, "You are registered!")


    @bot.message_handler(commands=['myinfo'])
    def my_info(message):
        user = db.get_user(message.from_user.id)
        info = f"User: {user['username']}\nMoney: {user['money']}\nAnimals: {user['animals']}\nProducts: {user['products']}"
        bot.send_message(message.chat.id, info)

    @bot.message_handler(commands=['buy'])
    def buy_animal(message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for animal in ['Cow', 'Pig', 'Rabbit', 'Chicken', 'Horse', 'Sheep', 'Goose']:
            markup.add(animal)
        msg = bot.reply_to(message, "Choose an animal to buy", reply_markup=markup)
        bot.register_next_step_handler(msg, process_buy)

    def process_buy(message):
        animal = message.text
        prices = {'Cow': 13000, 'Pig': 7000, 'Rabbit': 450, 'Chicken': 250, 'Horse': 45000, 'Sheep': 8000, 'Goose': 650}
        user = db.get_user(message.from_user.id)
        if user['money'] >= prices[animal]:
            user['money'] -= prices[animal]
            if animal in user['animals']:
                user['animals'][animal] += 1
            else:
                user['animals'][animal] = 1
            db.update_user(message.from_user.id, user)
            bot.send_message(message.chat.id, f"You bought a {animal}!")
        else:
            bot.send_message(message.chat.id, "Not enough money!")

    @bot.message_handler(commands=['sell'])
    def sell_product(message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for product in ['Cow Milk', 'Chicken Eggs', 'Sheep Wool']:
            markup.add(product)
        msg = bot.reply_to(message, "Choose a product to sell", reply_markup=markup)
        bot.register_next_step_handler(msg, process_sell)

    def process_sell(message):
        product = message.text
        prices = {'Cow Milk': randint(80, 110), 'Chicken Eggs': randint(80, 110), 'Sheep Wool': randint(900, 1020)}
        user = db.get_user(message.from_user.id)
        if product in user['products'] and user['products'][product] > 0:
            user['money'] += prices[product]
            user['products'][product] -= 1
            db.update_user(message.from_user.id, user)
            bot.send_message(message.chat.id, f"You sold {product}!")
        else:
            bot.send_message(message.chat.id, "Not enough products!")

    @bot.message_handler(commands=['cost'])
    def show_cost(message):
        prices = {
            'Cow': 13000,
            'Pig': 7000,
            'Rabbit': 450,
            'Chicken': 250,
            'Horse': 45000,
            'Sheep': 8000,
            'Goose': 650,
            'Cow Milk': '80-110',
            'Chicken Eggs': '80-110',
            'Sheep Wool': '900-1020'
        }
        cost_info = "Price List:\n"
        for item, price in prices.items():
            cost_info += f"{item}: {price}\n"
        bot.send_message(message.chat.id, cost_info)
