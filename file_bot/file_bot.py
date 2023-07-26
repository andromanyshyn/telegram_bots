import datetime
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from db.db_connect import Image, Session

from keys.keys import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
db = Dispatcher(bot=bot)


@db.message_handler(commands=["help"])
async def get_message_help(message: types.Message):
    help_text = """
    Here are the available commands:
    - /start: Start the bot and get a welcome message.
    - /files: Get options to view photos from the last week or last month.
    - /help: View this help message.
    """
    await message.reply(help_text)


@db.message_handler(commands=["start"])
async def get_message_start(message: types.Message):
    await message.reply("Hello! Welcome to the photo bot! Type '/help' to find out available commands")

    start_text = """
    This bot can save your photos and then you can 
    get all the photos in a certain period of time, 
    try to send a photo and the bot will save it    
    """
    await bot.send_message(
        message.chat.id, start_text
    )


@db.message_handler(commands=["files"])
async def get_message_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row(
        KeyboardButton("all photos for the last week "),
        KeyboardButton("all photos for the last month"),
    )

    await bot.send_message(message.chat.id, "choose the option", reply_markup=keyboard)


@db.message_handler(lambda message: message.text == "all photos for the last week")
async def last_week_photos(message: types.Message):
    ten_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=10)
    with Session() as session:
        images_last_ten_days = session.query(Image).filter(
            Image.date_created > ten_days_ago
        )
    for image in images_last_ten_days:
        try:
            await bot.send_photo(message.chat.id, image.image)
        except Exception as error:
            print(error)


@db.message_handler(lambda message: message.text == "all photos for the last month")
async def last_week_photos(message: types.Message):
    month_ago = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    with Session() as session:
        images_last_month = session.query(Image).filter(Image.date_created > month_ago)
    for image in images_last_month:
        await bot.send_photo(message.chat.id, image.image)


@db.message_handler(content_types=["photo"])
async def receive_image(message: types.Message):
    photo = message["photo"][-1]
    file_info = await bot.get_file(photo.file_id)
    new_photo = (await bot.download_file(file_info.file_path)).read()
    image = Image(image=new_photo)
    try:
        with Session() as session:
            session.add(image)
            session.commit()
        await bot.send_message(message.chat.id, "Photo is saved successfully")
    except Exception as error:
        logging.error(f"Помилка при збереженні фото: {error}")
        await bot.send_message(
            message.chat.id,
            "There was an error while saving the photo. Please try again later.",
        )


if __name__ == "__main__":
    executor.start_polling(dispatcher=db, skip_updates=True)
