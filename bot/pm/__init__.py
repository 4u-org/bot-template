from aiogram import Router
from bot.pm import start

router = Router()

router.include_router(start.router)