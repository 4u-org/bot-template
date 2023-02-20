import db.database as db
from aiogram import Bot, Dispatcher

async def main_shutdown(dispatcher: Dispatcher, *bots: Bot, bot: Bot):
    print("Shutdown started")
    # Shutdown code here
    await db.close()

    print ("Shutdown finished")