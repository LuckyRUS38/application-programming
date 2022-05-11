import telebot
import os
import random
import config

token = config.token

bot = telebot.TeleBot(token, parse_mode=None)


def get_random_cats(directory):
    files = os.listdir(directory)
    file_name = files[random.randint(0, len(files) - 1)]
    return file_name


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Я бот из Котляндии. Я высалаю различные картинки с котиками МЯУ!")


@bot.message_handler(commands=['white_cat', 'orange_cat', 'black_cat'])
def get_cat(message):
    command = message.text[1:]
    directories = {'white_cat': 'images/white_cats', 'orange_cat': 'images/orange_cats', 'black_cat': 'images/black_cats'}
    file_name = get_random_cats(directories[command])
    bot.send_photo(message.chat.id, photo=open(directories[command] + '/' + file_name, 'rb'))


bot.infinity_polling()
