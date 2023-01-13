import db.database as db
import db.models as models
from aiogram import Bot, Dispatcher

async def startup(dispatcher: Dispatcher, *bots: Bot, bot: Bot):
    print("Init started")
    # Init code here
    await db.migrate()
    await db.init()
    await models.Bot.update_or_create(
        id=bot.id,
        token=bot.token
    )
    
    print ("Init finished")