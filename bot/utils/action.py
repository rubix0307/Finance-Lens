import asyncio
from aiogram import Bot

class BotActionIndicator:
    def __init__(self, bot: Bot, chat_id: int, delay: float = 5.0, action: str = 'typing'):
        self.bot = bot
        self.chat_id = chat_id
        self.delay = delay
        self.action = action

    async def __aenter__(self):
        self.typing_task = asyncio.create_task(self._send_chat_action())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.typing_task.cancel()
        try:
            await self.typing_task
        except asyncio.CancelledError:
            pass

    async def _send_chat_action(self):
        while True:
            try:
                await self.bot.send_chat_action(chat_id=self.chat_id, action=self.action)
                await asyncio.sleep(self.delay)
            except Exception:
                break