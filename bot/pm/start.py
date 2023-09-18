from typing import Awaitable
from aiogram import Router, Bot, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.texts import TranslationTexts as texts

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
    if message.text == "/start":
        # Invoke with "/start"
        await message.answer(texts.HELLO_WORLD.value)
        return
        
    try:
        num = int(message.text[6:])
        await message.answer(texts.HELLO_WORLD_PLURALIZATION.value(num))
    except:
        await message.answer(texts.ERROR.value)

@router.message(F.text == texts.HELLO_WORLD.lazy)
async def command_start_handler(
    message: types.Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer(texts.HELLO_WORLD.value)
