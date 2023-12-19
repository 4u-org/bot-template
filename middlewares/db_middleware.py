import random
from typing import Any, Awaitable, Callable, Dict
import asyncio
from aiogram import types
from tortoise.exceptions import TransactionManagementError
import time

import tgtypes
from db import models
from middlewares.setup_middleware import SetupMiddleware

async def update_user_tg_info(user: types.User, retry: bool = True):
    try:
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
    except TransactionManagementError:
        # When user didn't exist, but was created in a different thread
        # Sorry, weird TortoiseORM errors, but I am too lazy to write a proper SQL
        if retry:
            await update_user_tg_info(user, False)

class DbMiddleware(SetupMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if "event_from_user" not in data:
            return await handler(event, data)
        
        update: types.Update = data["event_update"]
        update_type = update.event_type

        # Ignore group messages (don't get and update user info if message is not a command)
        # if (update_type == "message" and
        #     update.message.chat.type != "private" and
        #     (not update.message.text or not update.message.text.startswith("/"))):
        #     # Group chat non-command messages
        #     return await handler(event, data)
        
        user: types.User = data["event_from_user"]
        await update_user_tg_info(user)
        dbuser = await tgtypes.DbUser.create(user, data["bot"], data["state"])
        if update_type == "message" and update.message.chat.type == "private":
            dbuser.db.can_write = True
        data["user"] = dbuser

        r = await handler(event, data)
        await dbuser.db.save()
        return r