from aiogram import Router
from bot.pm import main, start, language, webapp

router = Router()
router.include_router(webapp.router)

router.include_router(start.router)
router.include_router(language.router)
router.include_router(main.router)