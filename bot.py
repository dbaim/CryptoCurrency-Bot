# import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher.middlewares import BaseMiddleware

from main import Currency
from config import TOKEN
from sqliter import SQLighter

import markups as nav

toggle = 3
f:bool = True


async def scheduled(result):
    await bot.send_message(Message.from_user.id, result)


# Инициализируем бота
bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot)


# Инициализируем БД
db = SQLighter('db.db')  

# Команда /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет, {0.first_name}! Этот телеграм бот нужен для отслеживания цен на валюты, криптовалюты и акции. Используйте меню навигации ниже'.format(
                               message.from_user), reply_markup=nav.mainMenu)


# Активация подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exist(message.from_user.id)):
        # Если юзера нет то создаем запись
        db.add_subscriber(message.from_user.id)
    else:
        # Если есть то обновляем статус
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы успешно подписаны.")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.message):
    if (not db.subscriber_exist(message.from_user.id)):
        # Если юзера нет добавляем его с не активнной подпиской
        db.add_subscriber(message.from_user.id, False)
    else:
        # Если был подписан то меняем статус
        db.update_subscription(message.from_user.id, False)
    await message.answer("Вы успешно отписаны.")

# Navigation:
@dp.message_handler(text="⬅️ Главное меню")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=nav.mainMenu)


@dp.message_handler(text="Криптовалюты")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите валюту ниже', reply_markup=nav.CryptoMenu)


@dp.message_handler(text="XRP")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'XRP', reply_markup=nav.xrpMenu)


@dp.message_handler(text="Посмотреть курс")
async def cmd_random(message: types.Message, toggle = 3):
    await bot.send_message(message.from_user.id, 'Курс проверяется')
    currency = Currency()
    while toggle != 0:
        if currency.get_result():
            try:
                answer = currency.get_answer()
                await bot.send_message(message.from_user.id, answer)
            except AttributeError:
                pass
        currency.check_currency()
        toggle -= 1


@dp.message_handler(text="Следить за курсом")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'Курс обновляется каждые 10 секунд')
    currency = Currency()
    while f:
        @dp.message_handler(text="Stop")
        async def cmd_random(message: types.Message):
            await bot.send_message(message.from_user.id, 'Возвращаюсь в Главное меню', reply_markup=nav.mainMenu)
            global f
            f = False
        if currency.get_result():
            try:
                answer = currency.get_answer()
                await bot.send_message(message.from_user.id, answer)
            except AttributeError:
                pass
        currency.check_currency()

if __name__ == '__main__':
    executor.start_polling(dp)
