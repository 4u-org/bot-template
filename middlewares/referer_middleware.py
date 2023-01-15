from typing import Any, Awaitable, Callable, Dict
from aiogram import types

import tgtypes
from middlewares.setup_middleware import SetupMiddleware

update_types = [
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
    "poll",
    "poll_answer",
    "my_chat_member",
    "chat_member",
    "chat_join_request"
]

class RefererMiddleware(SetupMiddleware):
    """
    Abstract referer middleware.
    """
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["referer"] = await self.get_referer(event, data)
        return await handler(event, data)

    async def get_referer(self, event: types.TelegramObject, data: Dict[str, Any]) -> int:
        """
        Detect current event referer based on event and context.

        **This method must be defined in child classes**

        :param event:
        :param data:
        :return:
        """
        pass

class SimpleRefererMiddleware(RefererMiddleware):
    async def get_referer(self, event: types.TelegramObject, data: Dict[str, Any]):
        update: types.Update = data["event_update"]
        update_type = update.event_type
        add = 0

        if update_type == "message":
            pass

        return (update_types.index(update_type) << 55) + add
