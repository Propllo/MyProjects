import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboard
from script import balance
from script import buy
import sqlite3

storage = MemoryStorage()
bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(filename='log.txt', level=logging.INFO)


class Buy(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


# -----Cостояние добавления--------
@dp.message_handler(Command('Купить'), state=None)
async def name_token(message: types.Message):
    await message.answer('Введите полное название токена: ')
    await Buy.q1.set()


@dp.message_handler(state=Buy.q1)
async def choice(message: types.Message, state=FSMContext):
    answer = message.text
    info_list = buy.Pars_Gecko(answer)
    if isinstance(info_list, list):
        await state.update_data(token=info_list[0])
        await state.update_data(price=info_list[1])
        await message.answer('Выберите добавление в: 1.Токенах; 2.Долларах')
        await Buy.q2.set()
    else:
        await bot.send_message(message.chat.id, text='Такой токен не найден', reply_markup=keyboard.start)
        await state.finish()


@dp.message_handler(state=Buy.q2)
async def count_tokens(message: types.Message, state=FSMContext):
    answer = message.text
    try:
        answer = int(message.text)
    except:
        await bot.send_message(message.chat.id, text='Должно быть целое число. Начните заново',
                               reply_markup=keyboard.start)
        await state.finish()
    if answer == 1 or answer == 2:
        await state.update_data(choice=answer)
        await message.answer('Введите кол-во:')
        await Buy.q3.set()
    else:
        await bot.send_message(message.chat.id, text='Такого нету. Начните заново', reply_markup=keyboard.start)
        await state.finish()


@dp.message_handler(state=Buy.q3)
async def mark(message: types.Message, state=FSMContext):
    answer = message.text
    answer = answer.replace(',', '.')
    try:
        answer = float(answer)
    except:
        await bot.send_message(message.chat.id, text='Это не число. Начните заново', reply_markup=keyboard.start)
        await state.finish()
    if answer >= 0:
        await state.update_data(count=answer)
        await message.answer('Введите пометку(кошелек):')
        await Buy.q4.set()
    else:
        await bot.send_message(message.chat.id, 'Если хотите убрать некоторое кол-во нажмите <Продать>',
                               reply_markup=keyboard.start)
        await state.finish()


@dp.message_handler(state=Buy.q4)
async def save_data(message: types.Message, state=FSMContext):
    answer = message.text
    await state.update_data(mark=answer)
    data = await state.get_data()
    token = data['token']
    price = data['price']
    choice = data['choice']
    count = data['count']
    mark = data['mark']
    await bot.send_message(message.chat.id, text=f'{data}')
    await state.finish()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.chat.id, text=f'Баланс:', reply_markup=keyboard.start,
                           parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message: types.Message):
    if message.text == 'Мой портфель':
        await bot.send_message(message.chat.id, text=f'Баланс: {balance.balance()} USD\n'
                                                     f'Портфель:\n'
                                                     f'{balance.my_portfolio()}', parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
