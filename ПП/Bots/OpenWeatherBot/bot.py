import telebot
import os
import random
import cfg
import requests
from datetime import datetime

token = cfg.token
bot = telebot.TeleBot(token, parse_mode=None)
localCNT = cfg.CNT
localUnits = cfg.UNITS
symbolAngle = {'imperial': '°F', 'metric': '℃'}
weather = {'01d': '☀', '02d': '⛅', '03d': '☁', '04d': '☁', '09d': '🌧', '10d': '💧', '11d': '⛈', '13d': '❄', '50d': '🌫'}

users = {}
main_keyboard = None
settings_keyboard = None
change_days_keyboard = None
change_units_keyboard = None

keyboards = {'main_menu': main_keyboard, 'settings_menu': settings_keyboard, 'change_days_menu': change_days_keyboard, 'change_units_menu': change_units_keyboard}


def generate_keyboard():
    global main_keyboard
    main_keyboard = telebot.types.ReplyKeyboardMarkup()
    key1 = telebot.types.KeyboardButton('⚙️НАСТРОЙКИ')
    key2 = telebot.types.KeyboardButton('💳ПОДДЕРЖАТЬ АВТОРА')
    key3 = telebot.types.KeyboardButton('🔍ПОМОЩЬ')
    main_keyboard.row(key1, key2)
    main_keyboard.row(key3)

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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    users[message.chat.id] = 'main_menu'
    bot.reply_to(message, "Чтобы начать пользоваться мной, и узнавать погоду вам нужно зайти с Telegram на телефоне, далее выслать в этот чат геопозицию, готово!", reply_markup=main_keyboard)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat=%s&lon=%s&appid=%s&mode=%s&lang=%s&units=%s&cnt=%s'
    urlForDecode = 'https://api.openweathermap.org/geo/1.0/reverse?lat=%s&lon=%s&limit=5&appid=%s'
    lat = message.location.latitude
    lon = message.location.longitude

    addressDecode = urlForDecode % (lat, lon, cfg.API_KEY)
    address = url % (lat, lon, cfg.API_KEY, cfg.MODE, cfg.LANG, localUnits, localCNT)
    responseDecode = requests.get(addressDecode)
    response = requests.get(address)
    if response.status_code == 200:
        data = response.json()
        dataDecode = responseDecode.json()
        bot.send_message(message.chat.id,
                         f"Ваше расположение - {dataDecode[0]['state']}, {dataDecode[0]['local_names']['ru']}"
                         f"\nИнформация о погоде на {localCNT} дней:\n")
        for i in range(0, localCNT):
            bot.send_message(message.chat.id,
                             f"Дата - {datetime.utcfromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m.%Y')}, {weather[data['list'][i]['weather'][0]['icon']]}{data['list'][i]['weather'][0]['description']} "
                             f"\nТемпература: \n  Минимальная: {data['list'][i]['temp']['min']}{symbolAngle[localUnits]}"
                             f"\n  Максимальная: {data['list'][i]['temp']['max']}{symbolAngle[localUnits]} "
                             f"\nДополнительная информация: \n  Время восхода - {datetime.utcfromtimestamp(int(data['list'][i]['sunset'])).strftime('%H:%M')}"
                             f"\n  Время захода - {datetime.utcfromtimestamp(int(data['list'][i]['sunrise'])).strftime('%H:%M')}")

        print('All good!')
    elif response.status_code == 401:
        print('Key protyx')
    elif response.status_code == 400:
        print('Bad requets')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global localCNT, localUnits
    if message.chat.id not in users:
        send_welcome(message)
        return
    elif message.text == '🔍ПОМОЩЬ' and users[message.chat.id] == 'main_menu':
        send_welcome(message)
        return
    elif message.text == '⚙️НАСТРОЙКИ' and users[message.chat.id] == 'main_menu':
        users[message.chat.id] = 'settings_menu'
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] ГЛАВНОЕ МЕНЮ --> ⚙️НАСТРОЙКИ (ВЫ ЗДЕСЬ)', reply_markup=settings_keyboard)
        return
    elif message.text == '💳ПОДДЕРЖАТЬ АВТОРА' and users[message.chat.id] == 'main_menu':
        bot.send_message(message.chat.id, 'Если у вас есть хоть какая-то копеечка, которой вы готовы поддержать автора, то можете их пожертвовать по ссылке. \nПЕРЕЙДЯ СЮДА --> https://donate.qiwi.com/payin/LuckyRUS38')
        return
    elif message.text == 'ИЗМЕНИТЬ КОЛИЧЕСТВО ДНЕЙ' and users[message.chat.id] == 'settings_menu':
        users[message.chat.id] = 'change_days_menu'
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] ГЛАВНОЕ МЕНЮ --> ⚙️НАСТРОЙКИ --> Изменение количества дней (ВЫ ЗДЕСЬ)', reply_markup=change_days_keyboard)
        return
    elif message.text == '↩️НАЗАД' and users[message.chat.id] == 'settings_menu':
        users[message.chat.id] = 'main_menu'
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] Вы вернулись в главное меню.', reply_markup=main_keyboard)
        return
    elif message.text == '↩️НАЗАД' and (users[message.chat.id] in ('change_days_menu', 'change_units_menu')):
        users[message.chat.id] = 'settings_menu'
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] Вы вернулись в меню настроек.', reply_markup=settings_keyboard)
        return
    elif message.text == 'ИЗМЕНИТЬ СИСТЕМУ ИЗМЕРЕНИЙ' and users[message.chat.id] == 'settings_menu':
        users[message.chat.id] = 'change_units_menu'
        bot.send_message(message.chat.id, '🧭[НАВИГАЦИЯ] ГЛАВНОЕ МЕНЮ --> ⚙️НАСТРОЙКИ --> Изменение системы измерений ВЫ ЗДЕСЬ)', reply_markup=change_units_keyboard)
        return
    elif message.text == '👑Имперская' and users[message.chat.id] == 'change_units_menu':
        localUnits = str('imperial')
        users[message.chat.id] = 'settings_menu'
        bot.send_message(message.chat.id, 'Вы успешно сменили систему измерений на ИМПЕРСКУЮ', reply_markup=settings_keyboard)
        return
    elif message.text == 'Ⓜ️Метрическая' and users[message.chat.id] == 'change_units_menu':
        localUnits = str('metric')
        users[message.chat.id] = 'settings_menu'
        bot.send_message(message.chat.id, 'Вы успешно сменили систему измерений на МЕТРИЧЕСКУЮ', reply_markup=settings_keyboard)
        return

    if users[message.chat.id] == 'change_days_menu':
        if message.text != '↩️НАЗАД':
            user_input = message.text
            if not user_input.isnumeric():
                bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуйте ещё раз. \nПодсказка: принимаются только целые числа от 1 до 16.', reply_markup=change_days_keyboard)
                return
            number = int(user_input)
            if number > 16 or number < 1:
                bot.send_message(message.chat.id, 'Количество дней не должно превышать 16-ти, а также не должно быть меньше 1-го.', reply_markup=change_days_keyboard)
                return
            else:
                localCNT = number
                users[message.chat.id] = 'settings_menu'
                bot.send_message(message.chat.id, f'Вы успешно изменили количество дней на {number}', reply_markup=settings_keyboard)
                return


generate_keyboard()
bot.infinity_polling()
