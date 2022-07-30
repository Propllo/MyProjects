import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import asyncio
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboard

storage = MemoryStorage()
bot = Bot(token=config.key_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(filename="log.txt", level=logging.INFO)


@dp.message_handler(commands='start', state=None)
async def welcome(message):
    """Вызываем меню и записываем id"""
    j_file = open('user.txt', 'w+')
    j_users = set()
    for line in j_file:
        j_users.add(line.strip())

    if not str(message.chat.id) in j_users:
        j_file = open('user.txt', 'a')  # 'a' по идее с конца
        j_file.write(str(message.chat.id) + '\n')
        j_users.add(message.chat.id)

    await bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}', reply_markup=keyboard.start,
                           parse_mode='Markdown')


@dp.message_handler(commands='info_py')
async def process_command_1(message: types.Message):
    """Вызываем инлайн кнопки"""
    await message.reply("Выберите что вас интересует: ", reply_markup=keyboard.inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    """Если была выбрана первая кнопка то получаем результат"""
    with open('info.txt', encoding='UTF-8') as f:
        file = f.read()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, file)


@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button2(callback_query: types.CallbackQuery):
    """Если была выбрана вторая кнопка то получаем результат"""
    with open('link_info.txt', encoding='UTF-8') as f:
        file2 = f.read()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, file2)


@dp.message_handler(commands='info')
async def cmd_test1(message: types.Message):
    await message.reply('Бот для обучения')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
