import logging

from aiogram import Bot, Dispatcher
from aiohttp import web

# compile translations
import subprocess
subprocess.call(['pybabel', 'compile', '-d', 'locales', '-D', 'messages'])

import bot as botsource
import web as websource
import middlewares
import config as cnf
import setup

dp = Dispatcher()
dp.include_router(botsource.router)

logger = logging.getLogger(__name__)

middlewares.db.setup(dp)
middlewares.referer.setup(dp)
middlewares.session.setup(dp)
middlewares.i18n.setup(dp)

# This function is called when bots are started (setup.start_bot)
# Bots won't start until this function's execution is over
dp.startup.register(setup.startup)

dp.shutdown.register(setup.shutdown)

def main() -> None:
    # Initialize Bot instance with an default parse mode which will be passed to all API calls
    app = web.Application(router=websource.router)
    bot = Bot(cnf.TOKEN, parse_mode="HTML")
    app["bot"] = bot
    setup.start_bot(dp, app, bot)

if __name__ == "__main__":
    main()