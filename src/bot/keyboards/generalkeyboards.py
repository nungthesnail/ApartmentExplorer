from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.utils.keyboard import KeyboardButton
from ..res import replicas


def keyboard_selecting_action() -> ReplyKeyboardMarkup:
    actions = replicas.get_inputs("selecting_action")
    key_row = [[KeyboardButton(text=action)] for action in actions]
    return ReplyKeyboardMarkup(keyboard=key_row, resize_keyboard=True)


def keyboard_selecting_city() -> ReplyKeyboardMarkup:
    cities = replicas.get_inputs("selecting_city")
    key_row = [[KeyboardButton(text=city)] for city in cities]
    return ReplyKeyboardMarkup(keyboard=key_row, resize_keyboard=True)


def keyboard_selecting_price() -> ReplyKeyboardMarkup:
    ranges = replicas.get_inputs("selecting_price")
    key_row = [[KeyboardButton(text=p_range)] for p_range in ranges]
    return ReplyKeyboardMarkup(keyboard=key_row, resize_keyboard=True)


def keyboard_selecting_platform() -> ReplyKeyboardMarkup:
    platforms = replicas.get_inputs("selecting_platform")
    key_row = [[KeyboardButton(text=platform)] for platform in platforms]
    return ReplyKeyboardMarkup(keyboard=key_row, resize_keyboard=True)
