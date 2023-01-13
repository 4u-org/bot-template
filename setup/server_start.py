from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from aiohttp import web

import config as cnf

async def set_main_bot_webhook(bot: Bot):
    await bot.set_webhook(cnf.BASE_URL + cnf.MAIN_BOT_PATH)

async def delete_main_bot_webhook(bot: Bot):
    await bot.delete_webhook()

def start_bot(dp: Dispatcher, app: web.Application, bot: Bot):
    dp.startup.register(set_main_bot_webhook)
    dp.shutdown.register(delete_main_bot_webhook)

    dp.fsm.storage = RedisStorage.from_url(cnf.REDIS_URL, key_builder=DefaultKeyBuilder(with_bot_id=True))

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=cnf.MAIN_BOT_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, port=cnf.WEB_SERVER_PORT)