import db.database as db
import db.models as models
from aiogram import Bot, Dispatcher
import config as cnf

async def main_startup(dispatcher: Dispatcher, *bots: Bot, bot: Bot):
    print("Init started")
    # Init code here
    if cnf.LOCAL:
        await bot.delete_webhook()
    else:
        await db.migrate()
        await bot.set_webhook(cnf.BASE_URL + cnf.MAIN_BOT_PATH)

    await db.init()
    await models.Bot.update_or_create(
        id=bot.id,
        token=bot.token
    )
    
    print ("Init finished")