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


def save_edit():
    keyboard = types.InlineKeyboardMarkup()
    save_btn = types.InlineKeyboardButton(text="Сохранить форму")
    edit_btn = types.InlineKeyboardButton(text="Отредактировать форму")
    keyboard.add(edit_btn, save_btn)
    return keyboard


def collisions_fix_markup(appendable=False):
    # варианты:
    # автоматическое исправление
    # исправление вручную
    # сохранить копию
    # отменить сохранение
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    auto_btn = types.InlineKeyboardButton(text="Автоматическое исправление", callback_data="auto")
    manually_btn = types.InlineKeyboardButton(text="Исправление вручную", callback_data="manually")
    save_btn = types.InlineKeyboardButton(text="Сохранить копию", callback_data="save")
    cancel_btn = types.InlineKeyboardButton(text="Отменить заполнение", callback_data="cancel")
    if appendable:
        keyboard.add(auto_btn, manually_btn, save_btn, cancel_btn)
    else:
        keyboard.add(manually_btn, save_btn, cancel_btn)
    return keyboard
