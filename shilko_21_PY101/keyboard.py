from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True)

info = types.KeyboardButton('/info_py')
stats = types.KeyboardButton('Stat')
inf_inl_1 = InlineKeyboardButton('Инфа пайтон: ', callback_data='button1')
inf_inl_2 = InlineKeyboardButton('Ссылки на инфу: ', callback_data='button2')
inline_kb1 = InlineKeyboardMarkup().add(inf_inl_1, inf_inl_2)

start.add(stats, info)
