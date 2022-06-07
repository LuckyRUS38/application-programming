import telebot
import os
import random
import cfg
import SQLConnect as sql

token = cfg.token

bot = telebot.TeleBot(token, parse_mode=None)

main_keyboard = None
cat_choice_keyboard = None
any_cat_keyboard = None
change_name_keyboard = None

keyboards = {'main_menu': main_keyboard, 'cat_choice_menu': cat_choice_keyboard, 'any_cat': any_cat_keyboard, 'change_name': change_name_keyboard}


def generate_keyboards():
    global main_keyboard
    main_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('Любой котик')
    key2 = telebot.types.KeyboardButton('Выбор котика')
    key3 = telebot.types.KeyboardButton('Помощь')
    key4 = telebot.types.KeyboardButton('Поменять имя')
    key5 = telebot.types.KeyboardButton('Добавить фото')
    main_keyboard.row(key1, key2)
    main_keyboard.row(key3, key4)
    main_keyboard.row(key5)

    global cat_choice_keyboard
    cat_choice_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('Белый кот ⚪️')
    key2 = telebot.types.KeyboardButton('Рыжий кот 🟠')
    key3 = telebot.types.KeyboardButton('Черный кот 🔳')
    key4 = telebot.types.KeyboardButton('Назад ↩️')
    cat_choice_keyboard.row(key1, key2, key3)
    cat_choice_keyboard.row(key4)

    global any_cat_keyboard
    any_cat_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('Назад ↩️')
    any_cat_keyboard.row(key1)


def send_cat(message, cat_color):
    sql.change_step(message.chat.id, 'cat_choice_menu')
    colors = {'white_cat': 'white', 'orange_cat': 'orange', 'black_cat': 'black'}
    file_name_list = sql.get_photos(1, colors[cat_color])
    # photos = []
    # for file_name in file_name_list:
    #     photos.append(telebot.types.InputMediaPhoto(open(cfg.photos_folder + file_name[0], 'rb')))

    bot.send_photo(message.chat.id, photo=open(cfg.photos_folder + file_name_list[0][0], 'rb'))


def get_random_file(directory):
    files = os.listdir(directory)
    file_name = files[random.randint(0, len(files) - 1)]
    return file_name


def check_user(chat_id):
    if not sql.is_user_exists(chat_id):
        sql.add_user(chat_id, 'main_menu', 3)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    check_user(message.chat.id)
    bot.send_message(message.chat.id, "Этот бот присылает картинки разных котиков:) Мррр...", reply_markup=main_keyboard)


@bot.message_handler(commands=['white_cat', 'black_cat', 'orange_cat'])
def get_cat(message):
    check_user(message.chat.id)
    command = message.text[1:]
    send_cat(message, command)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    check_user(message.chat.id)
    bot.send_message(message.chat.id, 'Теперь я знаю, где ты находишься 😝! Твои координаты: %s %s' % (
        message.location.longitude, message.location.latitude))


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    colors = {'upload_photo_w': 'white', 'upload_photo_o': 'orange', 'upload_photo_b': 'black'}
    step = sql.get_user_step(message.chat.id)
    if step in colors:
        color = colors[step]
        photo = message.photo[-1]
        fileID = photo.file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        path = cfg.photos_folder + fileID + '.jpg'
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        sql.add_new_filo(message.chat.id, color, fileID + '.jpg')
        bot.send_message(message.chat.id, 'Ваши котики успешно загружены', reply_markup=main_keyboard)
        sql.change_step(message.chat.id, 'main_menu')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    check_user(message.chat.id)
    user_step = sql.get_user_step(message.chat.id)

    if user_step == 'main_menu':
        match message.text:
            case 'Помощь':
                send_welcome(message)
                return
            case 'Поменять имя':
                sql.change_step(message.chat.id, 'change_name')
                bot.send_message(message.chat.id, 'Введите ваше новое имя',
                             reply_markup=any_cat_keyboard)
                return
            case 'Добавить фото':
                sql.change_step(message.chat.id, 'upload_step')
                bot.send_message(message.chat.id, 'Выберите цвет кота, которого вы хотите добавить',
                             reply_markup=cat_choice_keyboard)
                return
            case 'Выбор котика':
                sql.change_step(message.chat.id, 'cat_choice_menu')
                bot.send_message(message.chat.id, 'Выберите котика', reply_markup=cat_choice_keyboard)
                return
            case 'Любой котик':
                sql.change_step(message.chat.id, 'any_cat_menu')
                bot.send_message(message.chat.id, 'Введите количество котиков, которое вы хотите получить',
                                 reply_markup=any_cat_keyboard)
                return

    if user_step == 'cat_choice_menu':
        match message.text:
            case 'Белый кот ⚪️':
                send_cat(message, 'white_cat')
                return
            case 'Рыжий кот 🟠':
                send_cat(message, 'orange_cat')
                return
            case 'Черный кот 🔳':
                send_cat(message, 'black_cat')
                return

    match message.text:
        case 'Белый кот ⚪️' | 'Рыжий кот 🟠' | 'Черный кот 🔳':
            steps = {'Белый кот ⚪️': 'upload_photo_w', 'Рыжий кот 🟠': 'upload_photo_o', 'Черный кот 🔳': 'upload_photo_b'}
            sql.change_step(message.chat.id, steps[message.text])
            bot.send_message(message.chat.id, 'Ждём фотографию от вас.',
                             reply_markup=any_cat_keyboard)
            return

    if user_step in ('cat_choice_menu', 'any_cat_menu', 'upload_photo_b', 'upload_photo_o', 'upload_photo_w'):
        match message.text:
            case 'Назад ↩️':
                sql.change_step(message.chat.id, 'main_menu')
                bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=main_keyboard)
                return

    match user_step:
        case 'change_name':
            sql.change_name(message.chat.id, message.text)
            bot.send_message(message.chat.id, 'Ваше имя успешно изменено',
                             reply_markup=main_keyboard)
            sql.change_step(message.chat.id, 'main_menu')
            return
        case 'any_cat_menu':
            user_input = message.text
            if not user_input.isnumeric():
                bot.send_message(message.chat.id, 'Это не число, попробуйте ещё раз',
                                 reply_markup=any_cat_keyboard)
                return
            number = int(user_input)
            if number > 10 or number <= 0:
                bot.send_message(message.chat.id, 'Количество запрашиваемых котиков не должно превышать 10',
                                 reply_markup=any_cat_keyboard)
                return

            file_name_list = sql.get_photos(number)
            photos = []
            for file_name in file_name_list:
                photos.append(telebot.types.InputMediaPhoto(open(cfg.photos_folder + file_name[0], 'rb')))

            bot.send_media_group(message.chat.id, photos)
            bot.send_message(message.chat.id, 'Вот ваши котики', reply_markup=main_keyboard)
            sql.change_step(message.chat.id, 'main_menu')
            return

    bot.send_message(message.chat.id, 'Я вас не понял, попробуйте ещё раз', reply_markup=keyboards[user_step])


generate_keyboards()
bot.infinity_polling()
