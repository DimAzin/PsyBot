# KBT_terapist_bot OpenAI APIkey = "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"

import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import asyncio

# Ваши токены
# Получение токена из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Убедитесь, что переменная установлена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN set in environment variables")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Убедитесь, что переменная установлена
if not OPENAI_API_KEY:
    raise ValueError("No OPENAI_API_KEY set in environment variables")


# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher()

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

# Функция для отправки запроса в ChatGPT
async def send_request_to_chatgpt(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",  # Или используйте 'gpt-4', если доступно
            messages=[
                {"role": "system", "content": "assistant"},
                {"role": "user", "content": "Ты психолог с опытом в НЛП и КПТ более 5 лет. Проведи психологическую консультацию по запросу. " + prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Ошибка: {str(e)}"


# Маршрут для команды "/start"
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я твой робот-психолог. Напиши свой вопрос или описание проблемы и задай вопрос, что бы ты хотел получить в результате моей консультации. И я постараюсь тебе помочь.")


# Маршрут для обработки текстовых сообщений
@dp.message(F.text)
async def handle_message(message: types.Message):
    user_message = message.text
    prompt = f"Пользователь задал вопрос: {user_message}\nОтвет:"

    # Отправляем запрос в ChatGPT
    response = await send_request_to_chatgpt(prompt)

    # Отправляем ответ обратно пользователю
    await message.answer(response)


# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
