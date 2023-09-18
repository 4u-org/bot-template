import asyncio
import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import types
from datetime import datetime, timezone

import tgtypes
from middlewares.setup_middleware import SetupMiddleware

async def update_session(
    user: tgtypes.DbUser, 
    referer: int, 
    event: types.TelegramObject
) -> tgtypes.DbUser:
    if hasattr(event, "date"):
        update_time: datetime = event.date
    else:
        update_time = datetime.now(timezone.utc)
    await user.update_session(referer, update_time)

class SessionMiddleware(SetupMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if "user" in data and "referer" in data:
            await update_session(data["user"], data["referer"], event)
        return await handler(event, data)
