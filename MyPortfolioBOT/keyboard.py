from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True)

buy = types.KeyboardButton('/Купить')
sell = types.KeyboardButton('Продать')
portfolio = types.KeyboardButton('Мой портфель')
start.add(buy, sell)
start.add(portfolio)
