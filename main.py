from telebot import types
import telebot
import datetime as dt
from random import randint
import sqlite3

time = dt.datetime.now().strftime("%A %d-%B-%y %H:%M:%S")
nama, peringkat_teratas, uang = '', '', 50000
keinginan, hewan, jumlah, beli_hewan, jual_hewan = '', ['Sapi', 'Babi', 'Kelinci', 'Ayam', 'Kuda', 'Domba', 'Angsa'], 0, '', ''
waktu = [50, 35, 5, 10, 65, 45, 10]
bot = telebot.TeleBot('7477914057:AAF36unurvS0FNK7QlpxqXds5wRtdCeckaI')
harga_jual = {'Sapi': {1: randint(50000, 60000)},
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
harga_hewan = {'Sapi': randint(8500, 13000), 'Babi': randint(4500, 7000), 'Kelinci': randint(250, 450),
               'Ayam': randint(100, 250), 'Kuda': randint(35000, 45000), 'Domba': randint(6500, 8000),
               'Angsa': randint(450, 650)}
jumlah_hewan = {'Sapi': 0, 'Babi': 0, 'Kelinci': 0, 'Ayam': 0, 'Kuda': 0, 'Domba': 0,
                'Angsa': 0}
produk = {'Susu Sapi': 0, 'Telur Ayam': 0, 'Wol Domba': 0}
nama_hewan = ['Sapi: ', 'Babi: ', 'Kelinci: ', 'Ayam: ', 'Kuda: ', 'Domba: ', 'Angsa: ']
kutipan = ['Nasib adalah nasib, tetapi pilihan selalu ada padamu',
           'Kamu adalah apa yang kamu lakukan. Kamu adalah pilihanmu. Orang yang kamu jadikan dirimu.',
           'Ketika berdiri di depan pilihan, cukup lempar koin. Ini tidak akan memberikan jawaban yang benar, tetapi saat koin'
           'di udara, kamu sudah tahu apa yang kamu harapkan',
           'Dalam catur ini disebut "zugzwang", ketika ternyata langkah paling berguna adalah tidak bergerak sama sekali',
           'Pilihan yang benar dalam kenyataan tidak ada — hanya ada pilihan yang dibuat dan konsekuensinya',
           'Hidup kita adalah pilihan yang konstan: kepada siapa kita mempercayakan jari tanpa nama, dan kepada siapa jari tengah']
nama_pengguna, hewan_beli, hewan_tambah = '', '', ''
tambahan_hewan = []


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    if req[0] == '/help':
        bot.send_message(call.message.chat.id,
                         "Kamu memiliki peternakan dan modal awal, kamu perlu mengembangkan "
                         "peternakanmu dengan berbagai cara, karena ini adalah bisnis utamamu. Kamu bisa membeli "
                         "berbagai hewan, dari mereka kamu akan mendapatkan produk yang harus kamu jual "
                         "untuk menghasilkan uang dan meningkatkan diri, jangan lupa memeriksa harga jual "
                         "produkmua, mereka bisa berubah hampir setiap hari! (mungkin lebih baik membeli 2 "
                         "ayam daripada 1 sapi ;) Setiap bulan akan diadakan penilaian dan 3 peternak terbaik "
                         "akan mendapatkan bonus yang sesuai. Singkatnya, selamat mencoba! Perintah: /help - Tujuan"
                         " permainan, /reg - pendaftaran,  /top - daftar peternak terbaik, /cost - harga pembelian "
                         "hewan, /buy - membeli hewan, /myinfo - informasi utama kamu"
                         " /sell - menjual produk yang dimiliki.")
        bot.send_message(call.message.chat.id, f"«{kutipan[randint(0, len(kutipan) - 1)]}»",
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
        for i in harga_jual:
            d = []
            if a <= len(harga_jual) - 4:
                for u in harga_jual[i]:
                    d.append(str(u) + ': ' + str(harga_jual[i][u]) + ' IDR')
                d = ', '.join(d)
                s += hewan[a] + ': ' + d + "\n" + "\n"
            elif len(harga_jual) - 3 <= a < len(harga_jual) - 1:
                for u in harga_jual[i]:
                    d.append(str(u) + ': ' + str(harga_jual[i][u]) + ' IDR')
                d = ', '.join(d)
                s += i + ': ' + d + "\n" + "\n"
            else:
                for u in harga_jual[i]:
                    d.append(str(u) + ': ' + str(harga_jual[i][u]) + ' IDR')
                d = ', '.join(d)
                s += i + ': ' + d
            a += 1
        bot.send_message(call.message.chat.id, f'Berikut harga jualnya:\n\n{s}')
        sell(call.message)


@bot.message_handler(commands=['start'])
def start_message(message):
    global nama_pengguna, nama, uang, hewan_beli, hewan_tambah
    nama_pengguna = message.from_user.first_name
    con = sqlite3.connect('farmers.db')
    cur = con.cursor()
    result = cur.execute('''SELECT nama_pengguna FROM barang''').fetchall()
    st = 0
    for i in result:
        if nama_pengguna in i:
            st = 1
            break
    nama = cur.execute(f"SELECT nama FROM barang WHERE nama_pengguna = ?;""", (nama_pengguna,)).fetchone()
    if nama:
        nama = nama[0].strip()
    if st == 0 atau nama == '':
        bot.send_message(message.chat.id, f"Halo, {nama_pengguna}! "
                                          f"Kamu memiliki peternakan dan modal awal, kamu perlu mengembangkan "
                                          "peternakanmu dengan berbagai cara, karena ini adalah bisnis utamamu. Kamu bisa membeli "
                                          "berbagai hewan, dari mereka kamu akan mendapatkan produk yang harus kamu jual "
                                          "untuk menghasilkan uang dan meningkatkan diri, jangan lupa memeriksa harga jual "
                                          "produkmua, mereka bisa berubah hampir setiap hari! (mungkin lebih baik membeli 2 ayam, "
                                          "daripada 1 sapi ;) Setiap bulan akan diadakan penilaian dan 3 peternak terbaik "
                                          "akan mendapatkan bonus yang sesuai."
                                          "Singkatnya, selamat mencoba! Perintah: /help - Tujuan"
                                          " permainan, /reg - pendaftaran,  /top - daftar peternak terbaik,"
                                          "/cost - harga pada "
                                          "produk, /buy - membeli hewan, /myinfo - informasi utama kamu"
                                          " /sell - menjual produk yang dimiliki.")
        bot.send_message(message.chat.id, f"«{kutipan[randint(0, len(kutipan) - 1)]}»",
                         reply_markup=get_help_keyboard())
    else:
        unpack = cur.execute(f"SELECT * FROM barang WHERE nama_pengguna = ?;""", (nama_pengguna,)).fetchall()[0]
        uang, hewan_beli, hewan_tambah = unpack[2], unpack[3], unpack[4]

        bot.send_message(message.chat.id,
                         f"Halo, {nama}! Kamu memiliki peternakan dan modal awal,"
                         f"kamu perlu mengembangkan "
                         "peternakanmu dengan berbagai cara, karena ini adalah bisnis utamamu. Kamu bisa membeli "
                         "berbagai hewan, dari mereka kamu akan mendapatkan produk yang harus kamu jual "
                         "untuk menghasilkan uang dan meningkatkan diri, jangan lupa memeriksa harga jual "
                         "produkmua, mereka bisa berubah hampir setiap hari! (mungkin lebih baik membeli 2 ayam, "
                         "daripada 1 sapi ;) Setiap bulan akan diadakan penilaian dan 3 peternak terbaik "
                         "akan mendapatkan bonus yang sesuai."
                         "Singkatnya, selamat mencoba! Perintah: /help - Tujuan"
                         " permainan, /reg - pendaftaran,  /top - daftar peternak terbaik,"
                         "/cost - harga pada "
                         "produk, /buy - membeli hewan, /myinfo - informasi utama kamu"
                         " /sell - menjual produk yang dimiliki.")
        bot.send_message(message.chat.id, f"«{kutipan[randint(0, len(kutipan) - 1)]}»",
                         reply_markup=get_help_keyboard())
    con.commit()
    cur.close()
    con.close()


@bot.message_handler(commands=['reg'])
def registration(message):
    global nama_pengguna, nama, uang, beli_hewan, jumlah_hewan
    con = sqlite3.connect('farmers.db')
    cur = con.cursor()
    result = cur.execute('''SELECT nama_pengguna FROM barang''').fetchall()
    st = 0
    for i in result:
        if nama_pengguna in i:
            st = 1
            break
    if st == 0:
        cur.execute('INSERT INTO barang VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (nama_pengguna, nama, uang, beli_hewan,
                                                                                 jumlah_hewan['Sapi'], jumlah_hewan['Babi'],
                                                                                 jumlah_hewan['Kelinci'],
                                                                                 jumlah_hewan['Ayam'],
                                                                                 jumlah_hewan['Kuda'],
                                                                                 jumlah_hewan['Domba'],
                                                                                 jumlah_hewan['Angsa'],
                                                                                 dt.datetime.now()))
        con.commit()
        bot.send_message(message.chat.id, 'Registrasi berhasil! Sekarang kamu dapat mulai mengelola peternakanmu.',
                         reply_markup=get_help_keyboard())
    else:
        bot.send_message(message.chat.id, 'Kamu sudah terdaftar!',
                         reply_markup=get_help_keyboard())
    cur.close()
    con.close()


@bot.message_handler(commands=['top'])
def top(message):
    con = sqlite3.connect('farmers.db')
    cur = con.cursor()
    result = cur.execute('''SELECT nama_pengguna, uang FROM barang ORDER BY uang DESC LIMIT 10''').fetchall()
    s = ''
    for i in result:
        s += f'{i[0]} - {i[1]} IDR\n'
    bot.send_message(message.chat.id, f'Berikut daftar peternak terbaik:\n\n{s}',
                     reply_markup=get_help_keyboard())
    con.commit()
    cur.close()
    con.close()


@bot.message_handler(commands=['cost'])
def cost(message):
    global harga_hewan
    s = ''
    for i in harga_hewan:
        s += f'{i}: {harga_hewan[i]} IDR\n'
    bot.send_message(message.chat.id, f'Berikut daftar harga pembelian hewan:\n\n{s}',
                     reply_markup=get_help_keyboard())


@bot.message_handler(commands=['buy'])
def buy(message):
    keyboard = types.InlineKeyboardMarkup()
    for i in hewan:
        keyboard.add(types.InlineKeyboardButton(text=f'Beli {i}', callback_data=f'/buy_{i}'))
    bot.send_message(message.chat.id, 'Pilih hewan yang ingin dibeli:', reply_markup=keyboard)


@bot.message_handler(commands=['myinfo'])
def myinfo(message):
    global nama, uang, hewan_beli, hewan_tambah
    con = sqlite3.connect('farmers.db')
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM barang WHERE nama_pengguna = ?;""", (message.from_user.first_name,)).fetchall()
    if result:
        unpack = result[0]
        nama, uang, hewan_beli, hewan_tambah = unpack[1], unpack[2], unpack[3], unpack[4]
        hewan_milik = unpack[5:]
        s = f'Nama: {nama}\nUang: {uang} IDR\n\nHewan yang dimiliki:\n'
        for i, j in enumerate(hewan_milik):
            s += f'{hewan[i]}: {j}\n'
        bot.send_message(message.chat.id, f'Informasi utama kamu:\n\n{s}',
                         reply_markup=get_help_keyboard())
    else:
        bot.send_message(message.chat.id, 'Kamu belum terdaftar. Gunakan perintah /reg untuk mendaftar.',
                         reply_markup=get_help_keyboard())
    con.commit()
    cur.close()
    con.close()


@bot.message_handler(commands=['sell'])
def sell(message):
    global produk
    s = ''
    for i in produk:
        s += f'{i}: {produk[i]}\n'
    bot.send_message(message.chat.id, f'Berikut daftar produk yang dimiliki:\n\n{s}')
    bot.send_message(message.chat.id, 'Gunakan perintah /sell_{nama produk} untuk menjual produk.')


def get_help_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Tujuan permainan', callback_data='/help'))
    keyboard.add(types.InlineKeyboardButton(text='Daftar peternak terbaik', callback_data='/top'))
    keyboard.add(types.InlineKeyboardButton(text='Harga pembelian hewan', callback_data='/cost'))
    keyboard.add(types.InlineKeyboardButton(text='Membeli hewan', callback_data='/buy'))
    keyboard.add(types.InlineKeyboardButton(text='Informasi utama', callback_data='/myinfo'))
    keyboard.add(types.InlineKeyboardButton(text='Menjual produk', callback_data='/sell'))
    return keyboard


bot.polling(none_stop=True)
