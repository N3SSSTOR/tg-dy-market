import asyncio 
import logging 
import sys 

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from motor.motor_asyncio import AsyncIOMotorClient

from config import TG_BOT_TOKEN, MONGODB_CONNECTION_URL 
from utils.middlewares import UpdateUsernameMiddleware, AntiFloodMiddleware
from handlers import commands, payments, nav, catalog, requirements
from handlers.staff import operator, admin


async def main():
    bot = Bot(TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) 
    dp = Dispatcher()

    dp.include_routers(
        commands.router, 
        nav.router,
        catalog.router,
        payments.router,
        requirements.router,
        operator.router, 
        admin.router,
    )

    dp.message.middleware(UpdateUsernameMiddleware())
    dp.message.middleware(AntiFloodMiddleware())
    dp.callback_query.middleware(UpdateUsernameMiddleware())

    cluster = AsyncIOMotorClient(MONGODB_CONNECTION_URL)
    db = cluster.dy_market 

    await bot.set_my_commands([
        BotCommand(command="/menu", description="Открыть меню"),
        BotCommand(command="/get_orders", description="Оплаченные заказы"),
    ])

    await bot.delete_webhook(True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExit")