from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_fastapi_server import (
    SimpleRequestHandler,
    setup_application,
)

from fastapi import FastAPI

import config


def register_main_bot(dp: Dispatcher, app: FastAPI, bot: Bot, **kwargs):
    dp.fsm.storage = RedisStorage.from_url(config.REDIS_URL, key_builder=DefaultKeyBuilder(with_bot_id=True))

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.MAIN_BOT_PATH)
    setup_application(app, dp, bot=bot)
