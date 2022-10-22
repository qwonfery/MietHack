import telebot
import os
from telebot.async_telebot import AsyncTeleBot
from web_markup import web_app_keyboard

from dotenv import load_dotenv
load_dotenv('.env')


bot = AsyncTeleBot(os.getenv('API_TOKEN'))


@bot.message_handler(commands=['start'])
async def start(msg):
    await bot.send_message(msg.chat.id, "Hello world!")


@bot.message_handler(commands=['web'])
async def web_start(msg):
    await bot.send_message(msg.chat.id, "НУ ты!!!...", reply_markup=web_app_keyboard())

if __name__ == '__main__':
    import asyncio
    asyncio.run(bot.polling())