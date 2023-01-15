from typing import Awaitable
from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.texts import TranslationTexts as texts

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
        await message.answer(texts.HELLO_WORLD())
        return
        
    args = message.text.split(" ")
    if not args[1].isnumeric():
        # Invoke with "/start Hola", "/start Hi"
        text = " ".join(args[1:])
        await message.answer(texts.HELLO_WORLD_PARAMS(hello_text=text))
        return

    num = int(args[1])
    text = " ".join(args[2:])
    if text == "":
        # Invoke with "/start 1", "/start 100"
        await message.answer(texts.HELLO_WORLD_PLURALIZATION(num))
    else:
        # Invoke with "/start 1 Hola", "/start 100 Hi"
        await message.answer(
            texts.HELLO_WORLD_PARAMS_PLURALIZATION(
                hello_text=text,
                worlds_plural=texts.WORLDS_PLURAL(num)
            )
        )
