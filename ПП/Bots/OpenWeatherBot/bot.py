import telebot
import os
import random
import cfg
import requests
from datetime import datetime

token = cfg.token

bot = telebot.TeleBot(token, parse_mode=None)
weather = {'01d': '☀', '02d': '⛅', '03d': '☁', '04d': '☁', '09d': '🌧', '10d': '💧', '11d': '⛈', '13d': '❄', '50d': '🌫'}

def get_random_cats(directory):
    files = os.listdir(directory)
    file_name = files[random.randint(0, len(files) - 1)]
    return file_name


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Чтобы начать пользоваться мной, и узнавать погоду вам нужно зайти с Telegram на телефоне, далее выслать в этот чат геопозицию, готово!")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat=%s&lon=%s&appid=%s&mode=%s&lang=%s&units=%s&cnt=%s'
    urlForDecode = 'https://api.openweathermap.org/geo/1.0/reverse?lat=%s&lon=%s&limit=5&appid=%s'
    lat = message.location.latitude
    lon = message.location.longitude

    addressDecode = urlForDecode % (lat, lon, cfg.API_KEY)
    address = url % (lat, lon, cfg.API_KEY, cfg.MODE, cfg.LANG, cfg.UNITS, cfg.CNT)
    responseDecode = requests.get(addressDecode)
    response = requests.get(address)
    if response.status_code == 200:
        data = response.json()
        dataDecode = responseDecode.json()
        bot.send_message(message.chat.id,
                         f"Ваше расположение - {dataDecode[0]['state']}, {dataDecode[0]['local_names']['ru']}, \nИнформация о погоде на 10 дней:\n")

        for i in range(0, cfg.CNT):
            bot.send_message(message.chat.id,
                             f"Дата - {datetime.utcfromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m.%Y')}, {weather[data['list'][i]['weather'][0]['icon']]}{data['list'][i]['weather'][0]['description']} "
                             f"\nТемпература: \n  Минимальная: {data['list'][i]['temp']['min']}℃"
                             f"\n  Максимальная: {data['list'][i]['temp']['max']}℃"
                             f"\nДополнительная информация \nВремя восхода - {datetime.utcfromtimestamp(int(data['list'][i]['sunset'])).strftime('%H:%M:%S')}"
                             f"\nВремя захода - {datetime.utcfromtimestamp(int(data['list'][i]['sunrise'])).strftime('%H:%M:%S')}")

        print('All good!')
    elif response.status_code == 401:
        print('Key protyx')
    elif response.status_code == 400:
        print('Bad requets')


bot.infinity_polling()
