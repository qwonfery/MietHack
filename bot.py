import json
import requests
import telebot
import os
from keyboa import Keyboa
from telebot import types
from telebot.async_telebot import AsyncTeleBot

import web_markup
from web_markup import web_app_keyboard

from dotenv import load_dotenv
load_dotenv('.env')


bot = AsyncTeleBot(os.getenv('API_TOKEN'))


@bot.message_handler(commands=['start'])
async def start(msg):
    keyboard = types.ReplyKeyboardRemove()
    await bot.send_message(msg.chat.id, "Hello world!", reply_markup=keyboard)


@bot.message_handler(commands=['web'])
async def web_start(msg):
    await bot.send_message(msg.chat.id, "НУ ты!!!...", reply_markup=web_app_keyboard())


@bot.message_handler(commands=['forms'])
async def forms_start(msg):
    # forms = ["Dorogi"]
    forms = requests.get('https://miet-hack-api.herokuapp.com/form-names').json()['names']
    keyboard = Keyboa(items=forms)
    await bot.send_message(msg.chat.id, "Выберите форму:", reply_markup=keyboard())
    bot.register_callback_query_handler(choose_form_callback, None)


async def choose_form_callback(callback: types.CallbackQuery):
    form_name = callback.data
    chat_id = callback.from_user.id
    await bot.send_message(chat_id, "Можете заполнять форму", reply_markup=web_markup.form_open(form_name))


if __name__ == '__main__':
    import asyncio
    asyncio.run(bot.polling())

