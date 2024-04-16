import contextlib
import time 

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class UpdateUsernameMiddleware(BaseMiddleware):

    last_update_time = time.time()

    def __init__(self, update_seconds_interval: int = (3600 / 4)):
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

            user_query = dict(_id=event.from_user.id)
            user = await data["db"].users.find_one(user_query) 

            if user["username"] != event.from_user.username:
                await data["db"].users.update_one(user_query,
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
        user = await data["db"].users.find_one(dict(_id=event.from_user.id))

        if user["perm"] >= self.perm:
            return await handler(event, data)