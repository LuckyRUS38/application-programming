import telebot
import os
import random
import config

token = config.token

bot = telebot.TeleBot(token, parse_mode=None)

main_keyboard = None
cat_choice_keyboard = None
any_cat_keyboard = None

users = {}

keyboards = {'main_menu': main_keyboard, 'cat_choice_menu': cat_choice_keyboard, 'any_cat': any_cat_keyboard}


def generate_keyboards():
    global main_keyboard
    main_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('Любой котик')
    key2 = telebot.types.KeyboardButton('Выбор котика')
    key3 = telebot.types.KeyboardButton('Помощь')
    main_keyboard.row(key1, key2)
    main_keyboard.row(key3)

    global cat_choice_keyboard
    cat_choice_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('Белый кот ⚪️')
    key2 = telebot.types.KeyboardButton('Рыжий кот 🟠')
    key3 = telebot.types.KeyboardButton('Чёрно-белый кот 🔳')
    key4 = telebot.types.KeyboardButton('Назад ↩️')
    cat_choice_keyboard.row(key1, key2, key3)
    cat_choice_keyboard.row(key4)

    global any_cat_keyboard
    any_cat_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('Назад ↩️')
    any_cat_keyboard.row(key1)

def send_cat(message, cat_color):
    users[message.chat.id] = 'cat_choice_menu'
    directories = {'white_cat': 'images/white_cats', 'orange_cat': 'images/orange_cats', 'black_cat': 'images/black_cats'}
    file_name = get_random_file(directories[cat_color])
    bot.send_photo(message.chat.id, photo=open(directories[cat_color] + '/' + file_name, 'rb'),
                   reply_markup=cat_choice_keyboard)


def get_random_file(directory):
    files = os.listdir(directory)
    file_name = files[random.randint(0, len(files) - 1)]
    return file_name


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    users[message.chat.id] = 'main_menu'
    bot.send_message(message.chat.id, "Этот бот присылает картинки разных котиков.", reply_markup=main_keyboard)


@bot.message_handler(commands=['white_cat', 'black_cat', 'orange_cat'])
def get_cat(message):
    command = message.text[1:]
    send_cat(message, command)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot.send_message(message.chat.id, 'Теперь я знаю, где ты находишься 😝! Твои координаты: %s %s' % (
        message.location.longitude, message.location.latitude))


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.id not in users:
        send_welcome(message)
        return
    if message.text == 'Помощь' and users[message.chat.id] == 'main_menu':
        send_welcome(message)
        return
    if message.text == 'Выбор котика' and users[message.chat.id] == 'main_menu':
        users[message.chat.id] = 'cat_choice_menu'
        bot.send_message(message.chat.id, 'Выберите котика', reply_markup=cat_choice_keyboard)
        return
    if message.text == 'Белый кот ⚪️' and users[message.chat.id] == 'cat_choice_menu':
        send_cat(message, 'white_cat')
        return
    if message.text == 'Рыжий кот 🟠' and users[message.chat.id] == 'cat_choice_menu':
        send_cat(message, 'orange_cat')
        return
    if message.text == 'Чёрно-белый кот 🔳' and users[message.chat.id] == 'cat_choice_menu':
        send_cat(message, 'black_cat')
        return
    if message.text == 'Назад ↩️' and (users[message.chat.id] in ('cat_choice_menu', 'any_cat_menu')):
        users[message.chat.id] = 'main_menu'
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=main_keyboard)
        return

    if message.text == 'Любой котик' and users[message.chat.id] == 'main_menu':
        users[message.chat.id] = 'any_cat_menu'
        bot.send_message(message.chat.id, 'Введите количество котиков, которое вы хотите получить', reply_markup=any_cat_keyboard)
        return
    if users[message.chat.id] == 'any_cat_menu':
        user_input = message.text
        if not user_input.isnumeric():
            bot.send_message(message.chat.id, 'Это не число, попробуйте ещё раз',
                             reply_markup=any_cat_keyboard)
            return
        number = int(user_input)
        if number >= 10 or number <= 0:
            bot.send_message(message.chat.id, 'Количество запрашиваемых котиков не должно превышать 10', reply_markup=any_cat_keyboard)
            return

        pictures = []
        folders = ['orange_cats', 'black_cats', 'white_cats']
        for folder in folders:
            files = os.listdir('images/'+folder)
            for file in files:
                pictures.append('images/' + folder + '/' + file)

        pictures_to_send = []

        for i in range(number):
            random_index = random.randint(1, len(pictures)) - 1
            pictures_to_send.append(pictures[random_index])
            pictures.pop(random_index)

        photos = []

        for pic in pictures_to_send:
            photos.append(telebot.types.InputMediaPhoto(open(pic, 'rb')))

        bot.send_media_group(message.chat.id, photos)
        bot.send_message(message.chat.id, 'Вот ваши котики', reply_markup=main_keyboard)
        users[message.chat.id] = 'main_menu'
        return

    bot.send_message(message.chat.id, 'Я вас не понял, попробуйте ещё раз', reply_markup=keyboards[users[message.chat.id]])

generate_keyboards()
bot.infinity_polling()
