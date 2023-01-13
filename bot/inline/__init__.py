from aiogram import Router
from bot.inline import ping

router = Router()
router.include_router(ping.router)