import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboard
from script import balance, data_script, buy, sell

storage = MemoryStorage()
bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(filename='log.txt', level=logging.INFO)


class Buy(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


class Sell(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()


# -----Cостояние добавления токенов--------
@dp.message_handler(Command('Купить'), state=None)
async def name_token(message: types.Message):
    """Функция ввода названия токена
    """
    await message.answer('Введите полное название токена: ')
    await Buy.q1.set()


@dp.message_handler(state=Buy.q1)
async def choice(message: types.Message, state=FSMContext):
    """Функция выбора добавления в токенах или долларах

    answer - название токена (str)
    info-list - найденая информация о токене (полное название + аббревиатура, цена за токен на теперешний момент) (list)
    """
    answer = message.text
    info_list = buy.Pars_Gecko(answer)  # цифры тоже отображают страницу!!!!
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
    """Функция принимающая кол-во токенов или долларов

    answer - выбор пользователя в чем пополнять (int)
    """
    answer = message.text
    try:
        answer = int(message.text)
    except:
        await bot.send_message(message.chat.id, text='Должно быть целое число. Начните заново',
                               reply_markup=keyboard.start)
        await state.finish()
    if answer == 1 or answer == 2:
        print(answer, 1)
        await state.update_data(choice=answer)
        await message.answer('Введите кол-во:')
        await Buy.q3.set()
    else:
        print(answer, 2)
        await bot.send_message(message.chat.id, text='Такого нету. Начните заново', reply_markup=keyboard.start)
        await state.finish()


@dp.message_handler(state=Buy.q3)
async def mark(message: types.Message, state=FSMContext):
    """Функция ввода заметки

    answer - кол-во токенов или долларов (float)
    """
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
    """Функция сохранения полученной информации если такова есть

    answer - заметка (str)
    """
    answer = message.text
    await state.update_data(mark=answer)
    data = await state.get_data()
    data_script.save_data(message.chat.id, data)
    await bot.send_message(message.chat.id, text=f'Баланс: {balance.total_money()}$\nВаше последнее изменение внесено',
                           reply_markup=keyboard.start,
                           parse_mode='Markdown')
    await state.finish()


# ------Состояние изменения--------
@dp.message_handler(Command('Продать'), state=None)
async def choice_token(message: types.Message):
    info = sell.dict_token(message.chat.id)
    if isinstance(info, dict):
        info = str(info)
        info = info.replace('{', '')
        info = info.replace('}', '')
        info = info.replace(',', ';')
        await message.answer(f'Выберете номер токена или 0 для отмены:\n'
                             f'{info}')
        await Sell.q1.set()
    else:
        await bot.send_message(message.chat.id, text='У вас нету ничего для изменения.', reply_markup=keyboard.start)


@dp.message_handler(state=Sell.q1)
async def choice(message: types.Message, state=FSMContext):
    info = sell.dict_token(message.chat.id)
    try:
        answer = info[int(message.text)]
    except:
        await bot.send_message(message.chat.id, text='Такого нет. Введите число из предложенного списка.',
                               reply_markup=keyboard.start)
        await Sell.q1.set()
    else:
        await state.update_data(token=answer)
        price = buy.Pars_Gecko(answer[:answer.find('(')])
        await state.update_data(prise=price[1])
        await message.answer('Выберите изменение в: 1.Токенах; 2.Долларах')
        await Sell.q2.set()


@dp.message_handler(state=Sell.q2)
async def count_tokens(message: types.Message, state=FSMContext):
    """Функция принимающая кол-во токенов или долларов

    answer - выбор пользователя в чем пополнять (int)
    """
    answer = message.text
    try:
        answer = int(answer)
    except:
        await bot.send_message(message.chat.id, text='Введите число...', reply_markup=keyboard.start)
        await Sell.q2.set()
    if answer == 1 or answer == 2:
        await state.update_data(choice=answer)
        await message.answer('Введите кол-во:')
        await Sell.q3.set()
    else:
        await bot.send_message(message.chat.id, text='Такого выбора нету. Перевыберите', reply_markup=keyboard.start)
        await Sell.q2.set()


@dp.message_handler(state=Sell.q3)
async def save_data2(message: types.Message, state=FSMContext):
    answer = message.text
    print(answer)
    answer = answer.replace(',', '.')
    try:
        answer = float(answer)
    except:
        await bot.send_message(message.chat.id, text='Должно быть число. Перевыберите.', reply_markup=keyboard.start)
        await Sell.q3.set()
    if answer >= 0:
        await state.update_data(count=answer)
        data = await state.get_data()
        print(data)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Число не должно быть меньше нуля. Перевыберите',
                               reply_markup=keyboard.start)
        await Sell.q3.set()
# ------

@dp.message_handler(commands='start')
async def start(message: types.Message):
    """Функция начала работы бота по команде (start)
    """
    await bot.send_message(message.chat.id, text=f'Баланс: {str(balance.total_money(message.chat.id))}$',
                           reply_markup=keyboard.start,
                           parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message: types.Message):
    """Функция отклика при нажатии на Reply-кнопку
    """
    if message.text == 'Мой портфель':
        await bot.send_message(message.chat.id, text=f'Баланс: {balance.total_money(message.chat.id)}$\n'
                                                     f'Портфель:\n'
                                                     f'{balance.check_db(message.chat.id)}', parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
