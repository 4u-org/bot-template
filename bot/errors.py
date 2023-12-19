from datetime import datetime
import traceback
from aiogram import Router, F
from aiogram.types import ErrorEvent, Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import ExceptionTypeFilter, ExceptionMessageFilter
from aiogram.utils import markdown

from utils.texts import TranslationTexts as texts

router = Router()

class Limiter():
    last_minute: int = 0
    last_minute_count: int = 0

    def __init__(self, limit: int):
        self.limit = limit

    def check(self, text: str):
        time = datetime.now()
        if time.minute == self.last_minute:
            self.last_minute_count += 1
        else:
            self.last_minute_count = 1
            self.last_minute = time.minute

        return self.last_minute_count <= self.limit
    
limit = Limiter(10)

# Reduce annoying output (TODO: replace print with logger)
# @router.error(ExceptionTypeFilter(TelegramRetryAfter))
# async def handle_my_custom_exception(event: ErrorEvent):
#     print(event.exception)
# 
# @router.error(ExceptionTypeFilter(TelegramForbiddenError))
# async def handle_forbidden(event: ErrorEvent):
#     print(event.exception)
#     
# @router.error(ExceptionMessageFilter("HTTP Client says - Request timeout error"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     print(event.exception)
#     pass
# @router.error(ExceptionMessageFilter("HTTP Client says - ServerDisconnectedError: Server disconnected"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     print(event.exception)
#     pass

# Silence annoying errors
# @router.error(ExceptionMessageFilter("Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     pass
# @router.error(ExceptionMessageFilter("Telegram server says - Bad Request: query is too old and response timeout expired or query ID is invalid"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     pass
# @router.error(ExceptionMessageFilter("Telegram server says - Bad Request: MESSAGE_ID_INVALID"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     pass
# @router.error(ExceptionMessageFilter("Telegram server says - Bad Request: message to edit not found"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     pass
# 
# @router.error(ExceptionMessageFilter("Telegram server says - Bad Request: not enough rights to send text messages to the chat"))
# async def handle_my_custom_exception(event: ErrorEvent):
#     pass

# Example how to handle errors
# @router.error(F.update.message, F.update.message.as_("message"))
# async def handle_my_custom_exception(event: ErrorEvent, message: Message):
#     # do something with error
#     # await message.answer(texts.ERROR.value)
#     text = "Произошла ошибка:\n\n" + markdown.hcode(traceback.format_exc()[-3800:])
#     if limit.check(text):
#         await send_tech_message(text)
# 
# @router.error(F.update.query, F.update.query.as_("query"))
# async def handle_my_custom_exception(event: ErrorEvent, query: CallbackQuery):
#     # do something with error
#     await query.answer(texts.ERROR.value, show_alert=True)
#     text = "Произошла ошибка:\n\n" + markdown.hcode(traceback.format_exc()[-3800:])
#     if limit.check(text):
#         await send_tech_message(text)
# 
# 
# @router.error()
# async def error_handler(event: ErrorEvent):
#     text = "Произошла ошибка:\n\n" + markdown.hcode(traceback.format_exc()[-3800:])
#     if limit.check(text):
#         await send_tech_message(text)