import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

project_root = '/root/bot/'
sys.path.append(project_root)
os.chdir(project_root)

load_dotenv('.env')
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