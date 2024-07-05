from telebot import types
import telebot
import datetime as dt
from random import randint
import sqlite3

time = dt.datetime.now().strftime("%A %d-%B-%y %H:%M:%S")
name, topplace, money = '', '', 50000
desire, animals, count, buyan, sell_it = '', ['Sapi', 'Babi', 'Kelinci', 'Ayam', 'Kuda', 'Domba', 'Angsa'], 0, \
    '', ''
time = [50, 35, 5, 10, 65, 45, 10]
bot = telebot.TeleBot('TOKEN')
sell_dict = {'Sapi': {1: randint(50000, 60000)},
             'Babi': {1: randint(22000, 27000)},
             'Kuda': {1: randint(120000, 150000)},
             'Kelinci': {1: randint(800, 1000)},
             'Ayam': {1: randint(500, 800)},
             'Angsa': {1: randint(1900, 2100)},
             'Domba': {1: randint(32000, 34000)},
             'Susu Sapi (liter)': {1: randint(80, 110), 100: randint(5000, 6000), 300: randint(10500, 12050),
                                   550: randint(14000, 15200)},
             'Telur Ayam (lusin)': {1: randint(80, 110), 50: randint(3450, 3700),
                                    100: randint(5900, 6200),
                                    200: randint(9950, 10450)},
             'Wol Domba (kg)': {0.5: randint(480, 550), 1: randint(900, 1020),
                                5: randint(3900, 4150),
                                50: randint(26700, 27350)}}
dict = {'Sapi': randint(8500, 13000), 'Babi': randint(4500, 7000), 'Kelinci': randint(250, 450),
        'Ayam': randint(100, 250), 'Kuda': randint(35000, 45000), 'Domba': randint(6500, 8000),
        'Angsa': randint(450, 650)}
count_dict = {'Sapi': 0, 'Babi': 0, 'Kelinci': 0, 'Ayam': 0, 'Kuda': 0, 'Domba': 0,
              'Angsa': 0}
products = {'Susu Sapi': 0, 'Telur Ayam': 0, 'Wol Domba': 0}
animals_names = ['Sapi: ', 'Babi: ', 'Kelinci: ', 'Ayam: ', 'Kuda: ', 'Domba: ', 'Angsa: ']
phrases = ['Nasib adalah nasib, tetapi pilihan selalu ada padamu',
           'Kamu adalah apa yang kamu lakukan. Kamu adalah pilihanmu. Orang yang kamu ubah.',
           'Ketika dihadapkan pada pilihan, cukup lemparkan koin. Itu tidak akan memberikan jawaban yang benar, tetapi pada saat koin'
           'di udara, kamu sudah tahu apa yang kamu harapkan',
           'Dalam catur ini disebut "zugzwang", ketika ternyata gerakan yang paling berguna adalah tidak bergerak ke mana pun',
           'Tidak ada pilihan yang benar dalam kenyataan - hanya ada pilihan yang dibuat dan konsekuensinya',
           'Hidup kita adalah pilihan yang terus menerus: kepada siapa mempercayakan jari tanpa nama, dan kepada siapa jari tengah']
us_name, anm, ad_anm = '', '', ''
add_animals = []


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
        a, s = 0, ''
        for i in sell_dict:
            d = []
            if a <= len(sell_dict) - 4:
                for u in sell_dict[i]:
                    d.append(str(u) + ': ' + str(sell_dict[i][u]) + ' rupiah')
                d = ', '.join(d)
                s += animals[a] + ': ' + d + "\n" + "\n"
            elif len(sell_dict) - 3 <= a < len(sell_dict) - 1:
                for u in sell_dict[i]:
                    d.append(str(u) + ': ' + str(sell_dict[i][u]) + ' rupiah')
                d = ', '.join(d)
                s += i + ': ' + d + "\n" + "\n"
            else:
                for u in sell_dict[i]:
                    d.append(str(u) + ': ' + str(sell_dict[i][u]) + ' rupiah')
                d = ', '.join(d)
                s += i + ': ' + d
            a += 1
        bot.send_message(call.message.chat.id, f'Berikut adalah harga untuk penjualan:\n\n{s}')
        sell(call.message)


@bot.message_handler(commands=['start'])
def start_message(message):
    global us_name, name, money, anm, ad_anm
    us_name = message.from_user.first_name
    con = sqlite3.connect('petani.db')
    cur = con.cursor()
    result = cur.execute('''SELECT us_name FROM goods''').fetchall()
    st = 0
    for i in result:
        if us_name in i:
            st = 1
            break
    name = cur.execute(f"SELECT name FROM goods WHERE us_name = ?;""", (us_name,)).fetchone()
    if name:
        name = name[0].strip()
    if st == 0 atau name == '':
        bot.send_message(message.chat.id, f"Halo, {us_name}! "
                                          f"Kamu memiliki pertanian dan modal awal, kamu harus mengembangkan "
                                          "peternakanmu, karena itu adalah bisnis utama kamu. Kamu bisa membeli "
                                          "berbagai hewan, dari mereka akan langsung menghasilkan produk, yang harus "
                                          "kamu jual untuk mendapatkan uang dan berkembang, jangan lupa melihat"
                                          "harga untuk penjualanmu, "
                                          "mereka berubah hampir setiap hari! (mungkin lebih baik membeli 2 ayam, "
                                          "daripada 1 sapi ;) Setiap bulan akan diumumkan hasil dan 3 petani terbaik "
                                          "akan mendapatkan bonus sesuai ukuran."
                                          "Singkatnya, semangat! Perintah: /help - Deskripsi"
                                          " permainan, /reg - registrasi,  /top - daftar petani terbaik,"
                                          "/cost - harga untuk "
                                          "produk, /buy - pembelian hewan, /myinfo - informasi utama kamu"
                                          " /sell - penjualan produk yang ada.")
        bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                         reply_markup=get_help_keyboard())
    else:
        unpack = cur.execute(f"SELECT * FROM goods WHERE us_name = ?;""", (us_name,)).fetchall()[0]
        money, anm, ad_anm = unpack[2], unpack[3], unpack[4]

        bot.send_message(message.chat.id,
                         f"Halo, {name}! Kamu memiliki pertanian dan modal awal,"
                         f"kamu harus mengembangkan "
                         "peternakanmu, karena itu adalah bisnis utama kamu. Kamu bisa membeli "
                         "berbagai hewan, dari mereka akan langsung menghasilkan produk, yang harus "
                         "kamu jual untuk mendapatkan uang dan berkembang, jangan lupa melihat harga untuk "
                         "penjualanmu, mereka berubah hampir setiap hari! (mungkin lebih baik membeli 2 "
                         "ayam, daripada 1 sapi ;) Setiap bulan akan diumumkan hasil dan 3 petani terbaik "
                         "akan mendapatkan bonus sesuai ukuran. Singkatnya, semangat! Perintah: /help - Deskripsi"
                         " permainan, /reg - registrasi,  /top - daftar petani terbaik, /cost - harga untuk "
                         "produk, /buy - pembelian hewan, /myinfo - informasi utama kamu"
                         " /sell - penjualan produk yang ada.")
        bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                         reply_markup=get_help_keyboard())
    con.commit()
    con.close()


def get_help_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keys = ['/help', '/reg', '/top', '/cost', '/buy', '/myinfo', '/sell']
    keyboard.row(*(types.InlineKeyboardButton(key, callback_data=key) for key in keys))
    return keyboard


@bot.message_handler(commands=['reg'])
def registration(message):
    us_name = message.from_user.first_name
    con = sqlite3.connect('petani.db')
    cur = con.cursor()
    result = cur.execute('''SELECT us_name FROM goods''').fetchall()
    if not result or us_name not in [i[0] for i in result]:
        name = us_name
        cur.execute(f"""INSERT INTO goods (us_name, name, money, animals, ad_animals)
                    VALUES (?, ?, ?, ?, ?);""", (us_name, name, money, anm, ad_anm))
        con.commit()
        bot.send_message(message.chat.id, f"{us_name}, kamu berhasil mendaftar")
    else:
        bot.send_message(message.chat.id, f"{us_name}, kamu sudah terdaftar")
    con.close()


@bot.message_handler(commands=['top'])
def top(message):
    con = sqlite3.connect('petani.db')
    cur = con.cursor()
    result = cur.execute(f'''SELECT * FROM goods ORDER BY money DESC LIMIT 3;''').fetchall()
    top_message = "3 petani terbaik adalah:\n"
    for place, farmer in enumerate(result, start=1):
        top_message += f"{place}. {farmer[1]}: {farmer[2]} rupiah\n"
    bot.send_message(message.chat.id, top_message)
    con.close()


@bot.message_handler(commands=['cost'])
def cost(message):
    cost_message = "Harga untuk pembelian hewan adalah:\n"
    for animal, price in dict.items():
        cost_message += f"{animal}: {price} rupiah\n"
    bot.send_message(message.chat.id, cost_message)


@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_message(message.chat.id, "Hewan apa yang ingin kamu beli?",
                     reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True).add(*animals))


@bot.message_handler(func=lambda message: message.text in animals)
def handle_animal_choice(message):
    global buyan, money
    buyan = message.text
    price = dict[buyan]
    if money >= price:
        count_dict[buyan] += 1
        money -= price
        bot.send_message(message.chat.id,
                         f"Kamu berhasil membeli {buyan}. Kamu sekarang memiliki {count_dict[buyan]} {buyan}.")
    else:
        bot.send_message(message.chat.id,
                         f"Kamu tidak memiliki cukup uang untuk membeli {buyan}. Uang kamu saat ini: {money}.")


@bot.message_handler(commands=['myinfo'])
def myinfo(message):
    info_message = f"Informasi utama kamu:\nNama: {us_name}\nUang: {money} rupiah\nHewan: "
    for animal, count in count_dict.items():
        info_message += f"{animal}: {count}\n"
    info_message += "\nProduk:\n"
    for product, count in products.items():
        info_message += f"{product}: {count}\n"
    bot.send_message(message.chat.id, info_message)


@bot.message_handler(commands=['sell'])
def sell(message):
    sell_message = "Produk apa yang ingin kamu jual?\n"
    for product, count in products.items():
        sell_message += f"{product}: {count}\n"
    bot.send_message(message.chat.id, sell_message,
                     reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True).add(*products.keys()))


@bot.message_handler(func=lambda message: message.text in products)
def handle_sell_choice(message):
    global money
    product = message.text
    quantity = products[product]
    price = sell_dict[product][1]
    money += quantity * price
    products[product] = 0
    bot.send_message(message.chat.id, f"Kamu berhasil menjual {quantity} {product} seharga {quantity * price} rupiah. Uang kamu sekarang: {money}.")


bot.polling()
