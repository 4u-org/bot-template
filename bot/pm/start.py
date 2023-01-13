from typing import Awaitable
from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

router = Router()

@router.message(Command(commands=["start"]))
async def command_start_handler(
    message: types.Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer("Hellow world")
