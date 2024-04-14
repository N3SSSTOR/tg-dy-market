import asyncio 
import logging 
import sys 

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from motor.motor_asyncio import AsyncIOMotorClient

from config import TG_BOT_TOKEN, MONGODB_CONNECTION_URL 
from handlers import start, nav, catalog


async def main():
    bot = Bot(TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) 
    dp = Dispatcher()

    dp.include_routers(
        start.router, 
        nav.router,
        catalog.router,
    )

    cluster = AsyncIOMotorClient(MONGODB_CONNECTION_URL)
    db = cluster.dy_market 

    await bot.set_my_commands([
        BotCommand(command="/menu", description="Открыть меню")
    ])

    await bot.delete_webhook(True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExit")