import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

import django

load_dotenv('.env')
try:
    sys.path.append('/root/django/budget_lens')
    os.chdir('/root/django/budget_lens')
except FileNotFoundError:
    pass
django.setup()

BOT_TOKEN = os.getenv('BOT_TOKEN')

router = Router()
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    await dp.start_polling(bot, polling_timeout=180)

if __name__ == "__main__":
    from handlers import dp

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
