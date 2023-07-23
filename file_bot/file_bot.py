import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from keys.keys import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
db = Dispatcher(bot=bot)


@db.message_handler(commands=['start'])
async def get_message_start(message: types.Message):
    await message.reply('Привіт! Ласкаво просимо до мого бота!')
    await bot.send_message(message.chat.id, "Виберіть команду save для того щоб зберегти імена")


@db.message_handler(commands=['send'])
async def get_message_start(message: types.Message):
    with open('images/2023-07-23.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)


@db.message_handler(commands=['files'])
async def get_message_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row(
        KeyboardButton("all photos for the last week "), KeyboardButton("all photos for the last month")
    )

    await bot.send_message(message.chat.id, "choose the option", reply_markup=keyboard)


@db.message_handler(content_types=['photo'])
async def receive_image(message: types.Message):
    photo = message['photo'][-1]
    date_today = datetime.now().date()
    file_path = f'images/{date_today}.png'
    try:
        await photo.download(destination_file=file_path)
        await bot.send_message(message.chat.id, "Photo is saved successfully")
    except Exception as error:
        logging.error(f"Помилка при збереженні фото: {error}")
        await bot.send_message(message.chat.id, "Виникла помилка при збереженні фото. Спробуйте ще раз пізніше.")


if __name__ == '__main__':
    executor.start_polling(dispatcher=db, skip_updates=True)
