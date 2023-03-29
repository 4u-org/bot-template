from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from setup.startup import main_startup
from setup.shutdown import main_shutdown
from setup import local_register, server_register

import config

def register_main_bot(dp: Dispatcher, app: FastAPI, bot: Bot, **kwargs):
    if config.LOCAL:
        # TODO: replace with logger
        print("REGISTER LOCAL BOT (without redis)")
        local_register.register_main_bot(dp, app, bot, **kwargs)
    else:
        # TODO: replace with logger
        print("REGISTER WEBHOOK BOT (production ready)")
        server_register.register_main_bot(dp, app, bot, **kwargs)