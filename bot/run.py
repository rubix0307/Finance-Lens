import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

import django

load_dotenv('.env')
django.setup()

# project_root = '/root/bot/'

BOT_TOKEN = os.getenv('BOT_TOKEN')

router = Router()
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    from handlers import dp

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())