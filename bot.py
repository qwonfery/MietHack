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
    await bot.send_message(msg.chat.id, reply_markup=keyboard(), text="Выберите форму")
    bot.register_callback_query_handler(choose_form_callback, None)


@bot.message_handler(commands=['save'])
async def save_form(msg):
    r = requests.get(url=f"https://miet-hack-api.herokuapp.com/get-session/{msg.chat.id}")
    print(r.text)
    data = r.json()
    print("hey")
    r = requests.post(url="https://miet-hack-api.herokuapp.com/save-answer", data=data)
    response = r.json()['status']
    match response:
        #успешно
        case 201:
            await bot.send_message(msg.chat.id, text="Форма сохранена", reply_markup=types.ReplyKeyboardRemove())
        #дубликат
        case 400:
            await bot.send_message(msg.chat.id, text="Данные полностью совпадают с имеющимися", reply_markup=types.ReplyKeyboardRemove())
        #конфликт
        case 409:
            collisions = response['content']
            for collision in collisions:
                await bot.send_message(msg.chat.id, text=collision)
            await bot.send_message(msg.chat.id, text="Возникли следующие коллизии", reply_markup=web_markup.collisions_fix_markup())
            bot.register_callback_query_handler(choose_form_callback, data, collisions)
            #варианты:
            #автоматическое исправление
            #исправление вручную
            #сохранить копию
            #отменить сохранение


async def collisions_fix_callback(callback: types.CallbackQuery, form_data, collisions):
    option = callback.data
    chat_id = callback.from_user.id
    match option:
        case "auto":
            await auto_fix(chat_id, form_data, collisions)
        case "manually":
            await manually_fix(chat_id, form_data, collisions)
        case "save":
            await save_fix(chat_id, form_data)
        case "cancel":
            await cancel_fix(chat_id)


async def auto_fix(chat_id, form_data, collisions):
    # for collision in collisions:
    #    if collision
    pass


async def manually_fix(chat_id, form_data, collisions):
    for collision in collisions:
        # keyboard = Keyboa(items=[collision['field_value'] + "(старый)",collision['new_field_value'] + "(новый)"])
        change_str = f"Старое значение:{collision['field_value']}\nНовое значение: {collision['new_field_value']}"
        fields = requests.get(url=f"https://miet-hack-api.herokuapp.com/form/{form_data['name']}").json()['fields']
        await bot.send_message(chat_id, text="Выберите один из вариантов",
                               reply_markup=web_markup.collisions_fix_markup(fields[collision['field_id'] - 1]['field_type']))
        bot.register_callback_query_handler(choose_variant_callback, form_data, collision['field_id'])


async def choose_variant_callback(callback: types.CallbackQuery, form_data, field_id):

    chosen_value = callback.data
    form_data[field_id-1]['field-values'] = chosen_value
    chat_id = callback.from_user.id

    # await bot.send_message(chat_id, text="Принято", reply_markup=types.ReplyKeyboardRemove())


async def save_fix(chat_id, data):
    r = requests.post(url='https://miet-hack-api.herokuapp.com/save-answer', header={"force": "1"}, data=data)
    await bot.send_message(chat_id, text="Сохранено", reply_markup=types.ReplyKeyboardRemove())


async def cancel_fix(chat_id):
    await bot.send_message(chat_id, text="Отменено", reply_markup=types.ReplyKeyboardRemove())


async def choose_form_callback(callback: types.CallbackQuery):
    form_name = callback.data
    chat_id = callback.from_user.id
    await bot.send_message(chat_id, text="Можете заполнять форму", reply_markup=web_markup.form_open(form_name))


async def save_edit_callback(callback: types.CallbackQuery):
    name = callback.data
    chat_id = callback.from_user.id
    await bot.close()


if __name__ == '__main__':
    import asyncio
    asyncio.run(bot.polling())

