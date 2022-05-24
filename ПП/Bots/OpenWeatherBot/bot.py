import telebot
import cfg
import SQLConnect as sql
import requests
from datetime import datetime

# Initialize
token = cfg.token
bot = telebot.TeleBot(token, parse_mode=None)
symbolAngle = {'imperial': '°F', 'metric': '℃'}
systemUnits = {'imperial': 'узел', 'metric': 'м/с'}
weather = {'01d': '☀', '02d': '⛅', '03d': '☁', '04d': '☁', '09d': '🌧', '10d': '💧', '11d': '⛈', '13d': '❄', '50d': '🌫'}

# Keyboards
main_keyboard = None
settings_keyboard = None
change_days_keyboard = None
change_units_keyboard = None

keyboards = {'main_menu': main_keyboard, 'settings_menu': settings_keyboard, 'change_days_menu': change_days_keyboard,
             'change_units_menu': change_units_keyboard}

# Function Keyboard Generate


def generate_keyboard():
    global main_keyboard
    main_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('⚙️НАСТРОЙКИ')
    key2 = telebot.types.KeyboardButton('💳ПОДДЕРЖАТЬ АВТОРА')
    key3 = telebot.types.KeyboardButton('🔍ПОМОЩЬ')
    key4 = telebot.types.KeyboardButton('💡Обновления')
    main_keyboard.row(key1, key2)
    main_keyboard.row(key3, key4)

    global settings_keyboard
    settings_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('ИЗМЕНИТЬ КОЛИЧЕСТВО ДНЕЙ')
    key2 = telebot.types.KeyboardButton('ИЗМЕНИТЬ СИСТЕМУ ИЗМЕРЕНИЙ')
    key3 = telebot.types.KeyboardButton('↩️НАЗАД')
    settings_keyboard.row(key1)
    settings_keyboard.row(key2)
    settings_keyboard.row(key3)

    global change_days_keyboard
    change_days_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('↩️НАЗАД')
    change_days_keyboard.row(key1)

    global change_units_keyboard
    change_units_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('👑Имперская')
    key2 = telebot.types.KeyboardButton('Ⓜ️Метрическая')
    key3 = telebot.types.KeyboardButton('↩️НАЗАД')
    change_units_keyboard.row(key1, key2)
    change_units_keyboard.row(key3)


# Functions


def check_user(chat_id):
    if not sql.is_user_exists(chat_id):
        sql.add_user(chat_id, 'main_menu', 7, 'metric')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    check_user(message.chat.id)
    bot.reply_to(message, f"Чтобы начать пользоваться мной, и узнавать погоду вам нужно зайти с Telegram на телефоне,"
                          f" далее выслать в этот чат геопозицию, готово!", reply_markup=main_keyboard)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    check_user(message.chat.id)
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?lat=%s&lon=%s&appid=%s&mode=%s&lang=%s&units=%s&cnt=%s'
    urlForDecode = 'http://api.openweathermap.org/geo/1.0/reverse?lat=%s&lon=%s&limit=5&appid=%s'
    lat = message.location.latitude
    lon = message.location.longitude
    addressDecode = urlForDecode % (lat, lon, cfg.API_KEY)
    address = url % (lat, lon, cfg.API_KEY, cfg.MODE, cfg.LANG, sql.get_user_units(message.chat.id),
                     sql.get_user_days_qty(message.chat.id))
    responseDecode = requests.get(addressDecode)
    response = requests.get(address)
    if response.status_code == 200:
        data = response.json()
        dataDecode = responseDecode.json()
        bot.send_message(message.chat.id,
                         f"Ваше расположение - {dataDecode[0]['state']}, {dataDecode[0]['local_names']['ru']}"
                         f"\nИнформация о погоде на {sql.get_user_days_qty(message.chat.id)} дней:\n")
        for i in range(0, sql.get_user_days_qty(message.chat.id)):
            bot.send_message(message.chat.id,
                             f"Дата - {datetime.utcfromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m.%Y')},"
                             f" {weather[data['list'][i]['weather'][0]['icon']]}"
                             f"{data['list'][i]['weather'][0]['description']} "
                             f"\nТемпература: \n  Минимальная: {data['list'][i]['temp']['min']}"
                             f"{symbolAngle[sql.get_user_units(message.chat.id)]}"
                             f"\n  Максимальная: {data['list'][i]['temp']['max']}"
                             f"{symbolAngle[sql.get_user_units(message.chat.id)]} "
                             f"\nДополнительная информация: \n  Время восхода - "
                             f"{datetime.utcfromtimestamp(int(data['list'][i]['sunset'])).strftime('%H:%M')}"
                             f"\n  Время захода - "
                             f"{datetime.utcfromtimestamp(int(data['list'][i]['sunrise'])).strftime('%H:%M')}"
                             f"\n  Влажность - {data['list'][i]['humidity']}%"
                             f"\n  Скорость ветра - "
                             f"{data['list'][i]['speed']}{systemUnits[sql.get_user_units(message.chat.id)]}")

        print('All good!')
    elif response.status_code == 401:
        print('Key protyx')
    elif response.status_code == 400:
        print('Bad requets')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    check_user(message.chat.id)
    user_step = sql.get_user_step(message.chat.id)
    if message.text == '🔍ПОМОЩЬ' and user_step == 'main_menu':
        send_welcome(message)
        return
    elif message.text == '⚙️НАСТРОЙКИ' and user_step == 'main_menu':
        sql.change_step(message.chat.id, 'settings_menu')
        bot.send_message(message.chat.id, f'🧭[НАВИГАЦИЯ] ГЛАВНОЕ МЕНЮ --> ⚙️НАСТРОЙКИ (ВЫ ЗДЕСЬ)',
                         reply_markup=settings_keyboard)
        return
    elif message.text == '💳ПОДДЕРЖАТЬ АВТОРА' and user_step == 'main_menu':
        bot.send_message(message.chat.id,
                         'Если у вас есть хоть какая-то копеечка, которой вы готовы поддержать автора, '
                         'то можете их пожертвовать по ссылке.'
                         ' \nПЕРЕЙДЯ СЮДА --> https://donate.qiwi.com/payin/LuckyRUS38')
        return
    elif message.text == 'ИЗМЕНИТЬ КОЛИЧЕСТВО ДНЕЙ' and user_step == 'settings_menu':
        sql.change_step(message.chat.id, 'change_days_menu')
        bot.send_message(message.chat.id, f'🧭[НАВИГАЦИЯ] ГЛАВНОЕ МЕНЮ --> ⚙️НАСТРОЙКИ --> '
                                          f'Изменение количества дней (ВЫ ЗДЕСЬ)', reply_markup=change_days_keyboard)
        return
    elif message.text == '↩️НАЗАД' and user_step == 'settings_menu':
        sql.change_step(message.chat.id, 'main_menu')
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] Вы вернулись в главное меню.', reply_markup=main_keyboard)
        return
    elif message.text == '↩️НАЗАД' and (user_step in ('change_days_menu', 'change_units_menu')):
        sql.change_step(message.chat.id, 'settings_menu')
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] Вы вернулись в меню настроек.', reply_markup=settings_keyboard)
        return
    elif message.text == 'ИЗМЕНИТЬ СИСТЕМУ ИЗМЕРЕНИЙ' and user_step == 'settings_menu':
        sql.change_step(message.chat.id, 'change_units_menu')
        bot.send_message(message.chat.id, f'🧭[НАВИГАЦИЯ] ГЛАВНОЕ МЕНЮ --> ⚙️НАСТРОЙКИ --> '
                                          f'Изменение системы измерений ВЫ ЗДЕСЬ)', reply_markup=change_units_keyboard)
        return
    elif message.text == '👑Имперская' and user_step == 'change_units_menu':
        sql.change_units_system(message.chat.id, 'imperial')
        sql.change_step(message.chat.id, 'settings_menu')
        bot.send_message(message.chat.id, f'Вы успешно сменили систему измерений на ИМПЕРСКУЮ',
                         reply_markup=settings_keyboard)
        return
    elif message.text == 'Ⓜ️Метрическая' and user_step == 'change_units_menu':
        sql.change_units_system(message.chat.id, 'metric')
        sql.change_step(message.chat.id, 'settings_menu')
        bot.send_message(message.chat.id, f'Вы успешно сменили систему измерений на МЕТРИЧЕСКУЮ',
                         reply_markup=settings_keyboard)
        return
    elif message.text == '💡Обновления' and user_step == 'main_menu':
        bot.send_message(message.chat.id, f"В обновлении v2.0"
                                          f"\nДобавлены новые информативные данные, такие как скорость "
                                          f"ветра и влажность, которые "
                                          f"в зависимости от установленной вами системы измерений будут изменяться"
                                          f"\nВсе данные переведены на хранение в базу данных, теперь ваши"
                                          f" настройки не пропадут, и полностью индивидуальны."
                                          f"\n\nСпасибо что пользуетесь этим ботом и поддерживаете его денежкой:)")

    if user_step == 'change_days_menu':
        if message.text != '↩️НАЗАД':
            user_input = message.text
            if not user_input.isnumeric():
                bot.send_message(message.chat.id, f'Неправильный формат ввода, попробуйте ещё раз. '
                                                  f'\nПодсказка: принимаются только целые числа от 1 до 16.',
                                 reply_markup=change_days_keyboard)
                return
            number = int(user_input)
            if number > 16 or number < 1:
                bot.send_message(message.chat.id, 'Количество дней не должно превышать 16-ти, '
                                                  'а также не должно быть меньше 1-го.',
                                 reply_markup=change_days_keyboard)
                return
            else:
                sql.change_days_qty(message.chat.id, number)
                sql.change_step(message.chat.id, 'settings_menu')
                bot.send_message(message.chat.id, f'Вы успешно изменили количество дней на {number}',
                                 reply_markup=settings_keyboard)
                return


generate_keyboard()
bot.infinity_polling()
