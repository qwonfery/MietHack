import requests
from keyboa import Keyboa
from telebot import types


def web_app_keyboard():  # создание клавиатуры с webapp кнопкой
    keyboard = types.ReplyKeyboardMarkup(row_width=1)  # создаем клавиатуру
    web_app_test = types.WebAppInfo("https://f5uhuv.deta.dev/forms/Dorogi/new")  # создаем webappinfo - формат хранения url
    one_btn = types.KeyboardButton(text="Тестовая страница", web_app=web_app_test)  # создаем кнопку типа webapp
    keyboard.add(one_btn)  # добавляем кнопки в клавиатуру

    return keyboard  # возвращаем клавиатуру


def form_open(form_name):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)  # создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    web_app_test = types.WebAppInfo(f"https://f5uhuv.deta.dev/forms/{form_name}/new")  # создаем webappinfo - формат хранения url

    one_btn = types.InlineKeyboardButton(text="Форма", web_app=web_app_test)  # создаем кнопку типа webapp
    keyboard.add(one_btn)  # добавляем кнопки в клавиатуру
    return keyboard
