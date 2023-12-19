import db.database as db
import db.models as models
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramRetryAfter
import config

async def main_startup(dispatcher: Dispatcher, *bots: Bot, bot: Bot):
    print("Init started")
    # Init code here
    if config.LOCAL:
        await bot.delete_webhook()
    else:
        await db.migrate()
        try:
            await bot.set_webhook(
                url=config.BASE_URL + config.MAIN_BOT_PATH,
                allowed_updates=[
                    "message",
                    "edited_message",
                    "channel_post",
                    "edited_channel_post",
                    "inline_query",
                    "chosen_inline_result",
                    "callback_query",
                    "shipping_query",
                    "pre_checkout_query",
                    "poll",
                    "poll_answer",
                    "my_chat_member",
                    "chat_member",
                    "chat_join_request"],
            )
        except TelegramRetryAfter as e:
            print(f"WARNING, Bot webhook not set, retry after: {e.retry_after}")
        except Exception as e:
            print(e)

    await db.init()
    await models.Bot.update_or_create(
        id=bot.id,
        token=bot.token
    )
    
    print ("Init finished")