from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .handlers import start
from .handlers import general
import config
import asyncio


async def main():
    storage = MemoryStorage()

    bot = Bot(token=config.bot_token)
    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_router(start.router)
    dispatcher.include_router(general.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


def run():
    asyncio.run(main())
