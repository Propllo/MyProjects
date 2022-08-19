from aiogram import types

start = types.ReplyKeyboardMarkup(resize_keyboard=True)

buy = types.KeyboardButton('/Купить')
sell = types.KeyboardButton('/Продать')
portfolio = types.KeyboardButton('Мой портфель')
refresh = types.KeyboardButton('Обновить')
instruction = types.KeyboardButton('Инструкция')
start.add(portfolio, refresh)
start.add(buy, sell)
start.add(instruction)



