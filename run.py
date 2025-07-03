import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv
from app.handlers import router
import os

load_dotenv()
api_key = os.getenv("API_KEY")
bot = Bot(token=api_key)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")