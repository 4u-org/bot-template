import logging

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

# compile translations
import subprocess
subprocess.call(['pybabel', 'compile', '-d', 'locales', '-D', 'messages'])

import api
import bot as botsource
import middlewares
import config
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
dp.startup.register(setup.main_startup)

dp.shutdown.register(setup.main_shutdown)

app = FastAPI()
app.include_router(api.router)

# Initialize Bot instance with an default parse mode which will be passed to all API calls
bot = Bot(config.TOKEN, parse_mode="HTML")
setup.register_main_bot(dp, app, bot)
