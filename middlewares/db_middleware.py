from typing import Any, Awaitable, Callable, Dict
import asyncio
from aiogram import types
import time

import tgtypes
from db import models
from middlewares.setup_middleware import SetupMiddleware

class DbMiddleware(SetupMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        asyncio.create_task(models.TgUser.update_or_create(
            user_id=user.id,
            defaults={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "language_code": user.language_code,
                "is_premium": user.is_premium
            }
        ))
        dbuser = asyncio.create_task(tgtypes.DbUser.create(user, data["bot"]))
        data["dbuser"] = dbuser

        r = await handler(event, data)
        adbuser = await dbuser
        await adbuser.db.save()

        return r