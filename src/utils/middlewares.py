import contextlib
import datetime 
import time 

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class UpdateUsernameMiddleware(BaseMiddleware):

    last_update_time = time.time()

    def __init__(self, update_seconds_interval: int = (3600 / 2)):
        self.update_seconds_interval = update_seconds_interval

    async def __call__(
            self,
            handler: any,
            event: TelegramObject,
            data: dict[str, any],
    ) -> any:
        with contextlib.suppress(AttributeError):
            if event.text == "/start":
                return await handler(event, data)
        
        if (time.time() - self.last_update_time) > self.update_seconds_interval: 
            self.last_update_time = time.time()

            user_filter = {"_id": event.from_user.id}
            user = await data["db"].users.find_one(user_filter) 

            if user["username"] != event.from_user.username and not user["username"].startswith("guest_"):
                await data["db"].users.update_one(user_filter,
                    {
                        "$set": {"username": event.from_user.username}
                    }
                )        

        return await handler(event, data)


class PermProtectMiddleware(BaseMiddleware):

    def __init__(self, perm: int = 0) -> None:
        self.perm = perm 

    async def __call__(
            self,
            handler: any,
            event: TelegramObject,
            data: dict[str, any],
    ) -> any:
        user = await data["db"].users.find_one({"_id": event.from_user.id})

        if user["perm"] >= self.perm:
            return await handler(event, data)
        

class AntiFloodMiddleware(BaseMiddleware):
    time_updates: dict[int, datetime.datetime] = {}
    timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=2)

    async def __call__(
        self,
        handler: any,
        event: TelegramObject,
        data: dict[str, any],
    ) -> any:
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
            if user_id in self.time_updates.keys():
                if (datetime.datetime.now() - self.time_updates[user_id]) > self.timedelta_limiter:
                    self.time_updates[user_id] = datetime.datetime.now()
                    return await handler(event, data)
            else:
                self.time_updates[user_id] = datetime.datetime.now()
                return await handler(event, data)