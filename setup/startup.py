import db.database as db
import db.models as models
from aiogram import Bot, Dispatcher
import config

async def main_startup(dispatcher: Dispatcher, *bots: Bot, bot: Bot):
    print("Init started")
    # Init code here
    if config.LOCAL:
        await bot.delete_webhook()
    else:
        await db.migrate()
        await bot.set_webhook(config.BASE_URL + config.MAIN_BOT_PATH)

    await db.init()
    await models.Bot.update_or_create(
        id=bot.id,
        token=bot.token
    )
    
    print ("Init finished")