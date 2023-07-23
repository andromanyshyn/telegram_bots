import logging

from connect_db import database
from aiogram import Bot, Dispatcher, executor, types

from keys.keys import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
db = Dispatcher(bot=bot)


@db.message_handler(commands=['start'])
async def get_message_start(message: types.Message):
    await message.reply('Привіт! Ласкаво просимо до мого бота!')
    await bot.send_message(message.chat.id, "Виберіть команду save для того щоб зберегти імена")


@db.message_handler(commands=['save'])
async def save_username(message: types.Message):
    username = message.text.split()[1]
    if not username.isdigit():
        try:
            database.save_in_table(username)
        except Exception as error:
            await bot.send_message(message.chat.id, f'{error}')
        await bot.send_message(message.chat.id, f'Username is successfully saved')
    else:
        await bot.send_message(message.chat.id, f'Please write down correct username')


@db.message_handler(commands=['show'])
async def show_username(message: types.Message):
    usernames_list = database.show_in_table()
    await bot.send_message(message.chat.id, f'{usernames_list}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=db, skip_updates=True)
