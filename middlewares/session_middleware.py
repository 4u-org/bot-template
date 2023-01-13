import asyncio
import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import types
from datetime import datetime, timezone

import tgtypes
from middlewares.setup_middleware import SetupMiddleware

async def update_session(
    user: Awaitable[tgtypes.DbUser], 
    referer: int, 
    event: types.TelegramObject
) -> tgtypes.DbUser:
    auser = await user
    if hasattr(event, "date"):
        update_time: datetime = event.date
    else:
        update_time = datetime.now(timezone.utc)
    await auser.update_session(referer, update_time)
    return auser

class SessionMiddleware(SetupMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["dbuser"] = asyncio.create_task(update_session(data["dbuser"], data["referer"], event))
        return await handler(event, data)
