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
        if "event_from_user" not in data:
            return await handler(event, data)
        
        user: types.User = data["event_from_user"]
        await models.TgUser.update_or_create(
            user_id=user.id,
            defaults={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "language_code": user.language_code,
                "is_premium": user.is_premium
            }
        )
        dbuser = await tgtypes.DbUser.create(user, data["bot"])
        update: types.Update = data["event_update"]
        update_type = update.event_type
        if update_type == "message" and update.message.chat.type == "private":
            dbuser.db.can_write = True
        data["user"] = dbuser

        r = await handler(event, data)
        await dbuser.db.save()

        return r