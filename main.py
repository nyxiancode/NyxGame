from telebot import TeleBot, types
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['petani']  # Replace 'petani' with your database name
collection = db['goods']  # Collection name for storing 'goods' data

# Initialize TeleBot
bot = TeleBot('7477914057:AAF36unurvS0FNK7QlpxqXds5wRtdCeckaI')  # Replace with your bot token

# Global variables
phrases = [
    'Nasib adalah nasib, tetapi pilihan selalu ada padamu',
    'Kamu adalah apa yang kamu lakukan. Kamu adalah pilihanmu. Orang yang kamu ubah.',
    'Ketika dihadapkan pada pilihan, cukup lemparkan koin. Itu tidak akan memberikan jawaban yang benar, '
    'tetapi pada saat koin di udara, kamu sudah tahu apa yang kamu harapkan',
    'Dalam catur ini disebut "zugzwang", ketika ternyata gerakan yang paling berguna adalah tidak bergerak ke mana pun',
    'Tidak ada pilihan yang benar dalam kenyataan - hanya ada pilihan yang dibuat dan konsekuensinya',
    'Hidup kita adalah pilihan yang terus menerus: kepada siapa mempercayakan jari tanpa nama, dan kepada siapa jari tengah'
]

animals_names = ['Sapi: ', 'Babi: ', 'Kelinci: ', 'Ayam: ', 'Kuda: ', 'Domba: ', 'Angsa: ']

# Function to save data to MongoDB
def save_data(us_name, name, money, anm, ad_anm):
    data = {
        'us_name': us_name,
        'name': name,
        'money': money,
        'anm': anm,
        'ad_anm': ad_anm
    }
    collection.update_one({'us_name': us_name}, {'$set': data}, upsert=True)

# Function to retrieve data from MongoDB
def get_data(us_name):
    data = collection.find_one({'us_name': us_name})
    return data

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    if req[0] == '/help':
        bot.send_message(call.message.chat.id,
                         "Kamu memiliki pertanian dan modal awal, kamu harus mengembangkan "
                         "peternakanmu, karena itu adalah bisnis utama kamu. Kamu bisa membeli "
                         "berbagai hewan, dari mereka akan langsung menghasilkan produk, yang harus "
                         "kamu jual untuk mendapatkan uang dan berkembang, jangan lupa melihat harga untuk "
                         "penjualanmu, mereka berubah hampir setiap hari! (mungkin lebih baik membeli 2 "
                         "ayam, daripada 1 sapi ;) Setiap bulan akan diumumkan hasil dan 3 petani terbaik "
                         "akan mendapatkan bonus sesuai ukuran. Singkatnya, semangat! Perintah: /help - Deskripsi"
                         " permainan, /reg - registrasi,  /top - daftar petani terbaik, /cost - harga untuk "
                         "pembelian, /buy - pembelian hewan, /myinfo - informasi utama kamu"
                         " /sell - penjualan produk yang ada.")
        bot.send_message(call.message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                         reply_markup=get_help_keyboard())
    elif req[0] == '/top':
        top(call.message)
    elif req[0] == '/cost':
        cost(call.message)
    elif req[0] == '/buy':
        buy(call.message)
    elif req[0] == '/myinfo':
        myinfo(call.message)
    elif req[0] == '/sell':
        sell(call.message)

# Command handler to start the game or show registration message
@bot.message_handler(commands=['start'])
def start_message(message):
    us_name = message.from_user.first_name
    data = get_data(us_name)
    if data:
        name = data.get('name', '')
        money = data.get('money', 50000)
        anm = data.get('anm', '')
        ad_anm = data.get('ad_anm', '')
        bot.send_message(message.chat.id, f"Halo, {name}! Kamu memiliki {money} rupiah dan hewan {anm}.")
    else:
        bot.send_message(message.chat.id, f"Halo, {us_name}! Kamu belum terdaftar.")

# Command handler for registration
@bot.message_handler(commands=['reg'])
def registration(message):
    us_name = message.from_user.first_name
    name = message.text.split()  # Replace with appropriate input from user
    money = 50000  # Initial money
    anm = ''  # Initialize animals
    ad_anm = ''  # Initialize more animals
    save_data(us_name, name, money, anm, ad_anm)
    bot.send_message(message.chat.id, f"Oke, {name}, kamu sekarang terdaftar di permainan. Selamat bermain dan semoga sukses!")

# Function to create InlineKeyboardMarkup for help menu
def get_help_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keys = ['/help', '/reg', '/top', '/cost', '/buy', '/myinfo', '/sell']

    for key in keys:
        keyboard.add(types.InlineKeyboardButton(text=key, callback_data=key))

    return keyboard

# Function to handle '/top' command
@bot.message_handler(commands=['top'])
def top(message):
    data = collection.find().sort('money', -1).limit(3)
    top_message = "Top 3 petani:\n"
    for idx, doc in enumerate(data, 1):
        top_message += f"{idx}. {doc['name']} - {doc['money']} rupiah\n"
    bot.send_message(message.chat.id, top_message)

# Function to handle '/cost' command
@bot.message_handler(commands=['cost'])
def cost(message):
    s = ''
    for idx, animal in enumerate(animals_names, 1):
        s += f"{animal}: {idx * 1000} rupiah\n"  # Example cost calculation, replace with actual logic
    bot.send_message(message.chat.id, f'Harga untuk pembelian:\n\n{s}')

# Function to handle '/buy' command
@bot.message_handler(commands=['buy'])
def buy(message):
    keyboard = types.InlineKeyboardMarkup()
    for animal in animals_names:
        keyboard.add(types.InlineKeyboardButton(text=animal, callback_data=f'buy_{animal.split()[0]}'))
    bot.send_message(message.chat.id, "Pilih hewan yang ingin kamu beli:", reply_markup=keyboard)

# Function to handle '/myinfo' command
@bot.message_handler(commands=['myinfo'])
def myinfo(message):
    us_name = message.from_user.first_name
    data = get_data(us_name)
    if data:
        name = data.get('name', '')
        money = data.get('money', 50000)
        anm = data.get('anm', '')
        ad_anm = data.get('ad_anm', '')
        bot.send_message(message.chat.id, f'{name}, kamu memiliki {money} rupiah, hewan: {anm}, lebih banyak lagi: {ad_anm}')
    else:
        bot.send_message(message.chat.id, "Kamu belum terdaftar.")

# Function to handle '/sell' command
@bot.message_handler(commands=['sell'])
def sell(message):
    keyboard = types.InlineKeyboardMarkup()
    for idx, animal in enumerate(animals_names, 1):
        keyboard.add(types.InlineKeyboardButton(text=animal, callback_data=f'sell_{idx}'))
    bot.send_message(message.chat.id, "Pilih produk untuk dijual:", reply_markup=keyboard)

# Polling the bot to keep it running
bot.polling(none_stop=True)
