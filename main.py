import telebot
from telebot import types
import sqlite3
import requests
import json

bot = telebot.TeleBot('7034766821:AAEEv9V6xWgoORseMIGVcPmq1CeeUJHnDlg')
API = '1fb00bbb5d21452e8ec81530240804'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Узнать погоду')
    markup.row(button1)
    bot.send_message(message.chat.id, 'Привет, выбери, что ты хочешь сделать', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(content_types=['text'])
def on_click(message):
    if message.text == 'Узнать погоду':
        bot.send_message(message.chat.id, 'Введи название города')
        bot.register_next_step_handler(message, get_weather)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API}&q={city}&lang=ru')
    data = json.loads(weather.text)
    text = f'Температура: {int(data["current"]["temp_c"])}{chr(0xB0)}C\n{data["current"]["condition"]["text"]}\n'
    text += f'{message.from_user.first_name} молодец'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
