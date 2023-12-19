from aiogram import Router
from bot import pm, inline, errors

router = Router()
router.include_router(pm.router)
router.include_router(inline.router)
router.include_router(errors.router)