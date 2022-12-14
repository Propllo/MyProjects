import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboard
from script import balance, data_script, buy, sell, refresh, instruction

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
    if answer.isdigit():
        await message.answer('Введите название, а не число.')
        await Buy.q1.set()
    else:
        info_list = buy.pars_gecko(answer)  # цифры тоже отображают страницу!!!!
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
        await bot.send_message(message.chat.id, text='Должно быть целое число. Перевыберите')
        await Buy.q2.set()
    else:
        if answer == 1 or answer == 2:
            await state.update_data(choice=answer)
            await message.answer('Введите кол-во:')
            await Buy.q3.set()
        else:
            await bot.send_message(message.chat.id, text='Такого нету. Перевыберите')
            await Buy.q2.set()


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
        await bot.send_message(message.chat.id, text='Это не число. Перевыберите')
        await Buy.q3.set()
    if answer >= 0:
        await state.update_data(count=answer)
        await message.answer('Введите пометку(кошелек):')
        await Buy.q4.set()
    else:
        await bot.send_message(message.chat.id, 'Число не должно быть меньше нуля. Перевыберите')
        await Buy.q3.set()


@dp.message_handler(state=Buy.q4)
async def save_data(message: types.Message, state=FSMContext):
    """Функция сохранения полученной информации если такова есть

    answer - заметка (str)
    """
    answer = message.text
    await state.update_data(mark=answer)
    data = await state.get_data()
    data_script.save_data(message.chat.id, data)
    await bot.send_message(message.chat.id,
                           text=f'Баланс: {balance.total_money(message.chat.id)}$\nВаше последнее изменение внесено',
                           reply_markup=keyboard.start,
                           parse_mode='Markdown')
    await state.finish()


# ------Состояние изменения--------
@dp.message_handler(Command('Продать'), state=None)
async def choice_token(message: types.Message):
    """Функция проверяющая БД на наличие у id токенов и если таковые есть позволяет выбрать один из них

    info - словарь имен токенов (dict)
    """
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
        await bot.send_message(message.chat.id, text=f'{info}', reply_markup=keyboard.start)


@dp.message_handler(state=Sell.q1)
async def choice(message: types.Message, state=FSMContext):
    """Функция выбора изменения баланса токена

    info - список токенов (list)
    answer - выбранный токен (str)
    prise - список полученной информации о токене имя-цена (list)
    """
    info = sell.dict_token(message.chat.id)
    try:
        answer = info[int(message.text)]
    except:
        await bot.send_message(message.chat.id, text='Такого нет.',
                               reply_markup=keyboard.start)
        await state.finish()
    else:
        await state.update_data(token=answer)
        price = buy.pars_gecko(answer[:answer.find('(')])
        await state.update_data(price=price[1])
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
        await bot.send_message(message.chat.id, text='Введите число...')
        await Sell.q2.set()
    else:
        if answer == 1 or answer == 2:
            await state.update_data(choice=answer)
            await message.answer('Введите кол-во:')
            await Sell.q3.set()
        else:
            await bot.send_message(message.chat.id, text='Такого выбора нету. Перевыберите')
            await Sell.q2.set()


@dp.message_handler(state=Sell.q3)
async def save_data(message: types.Message, state=FSMContext):
    """Функция сохранения изменения о токене в БД

    answer - кол-во токенов или долларов (float)
    data - словарь выборов пользователя (dict)
    """
    answer = message.text
    answer = answer.replace(',', '.')
    try:
        answer = float(answer)
    except:
        await bot.send_message(message.chat.id, text='Должно быть число. Перевыберите.')
        await Sell.q3.set()
    if answer >= 0:
        await state.update_data(count=answer)
        data = await state.get_data()
        data_script.data_sell(message.chat.id, data)
        await bot.send_message(message.chat.id, text='Изменения добавлены', reply_markup=keyboard.start)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Число не должно быть меньше нуля. Перевыберите')
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
    """Функция отклика при нажатии на некоторые Reply-кнопки
    """
    if message.text == 'Мой портфель':
        await bot.send_message(message.chat.id, text=f'Баланс: {balance.total_money(message.chat.id)}$\n'
                                                     f'Портфель:\n'
                                                     f'{balance.check_db(message.chat.id)}', parse_mode='Markdown')
    elif message.text == 'Обновить':
        await bot.send_message(message.chat.id, text=f"{refresh.refresh(message.chat.id)}")
    elif message.text == 'Инструкция':
        await bot.send_message(message.chat.id, text=f"{instruction.read_inst()}", parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
