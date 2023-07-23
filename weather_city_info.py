import logging
import requests

from aiogram import Bot, Dispatcher, executor, types

from keys.keys import TOKEN
from keys.keys import OPENWEATHER_API_KEY

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
db = Dispatcher(bot=bot)


@db.message_handler(commands=['start'])
async def get_message_start(message: types.Message):
    await message.reply('Привіт! Цей Бот Вміє знаходити погоду за назвою міста!')
    await bot.send_message(message.chat.id, "Введіть назву міста - приклад 'London'")


@db.message_handler(content_types=types.ContentType.TEXT)
async def get_city_weather(message: types.Message):
    city_name = message.text
    city_weather = get_weather_info(city_name)
    if city_weather == 'city not found':
        await bot.send_message(message.chat.id, 'Введіть правильно назву міста')
    else:
        await bot.send_message(message.chat.id, f'{city_weather} Celcius')


def get_weather_info(city):
    response = requests.get(
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    data = response.json()
    if response.status_code == 200:
        return data['main']['temp']
    elif response.status_code == 404:
        return data['message']


if __name__ == '__main__':
    executor.start_polling(dispatcher=db)
