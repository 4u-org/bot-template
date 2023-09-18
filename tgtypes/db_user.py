from __future__ import annotations
from aiogram import types, Bot
from datetime import datetime

from db import models
import config

class DbUser():
    def __init__(self, db: models.User, bot: Bot, tg: types.User, first_interaction: bool = False):
        self.db = db
        self.bot = bot
        self.tg = tg
        self.first_interaction = first_interaction

    class Config:
        arbitrary_types_allowed = True
    
    async def create(user: types.User, bot: Bot) -> DbUser:
        db, first_interaction = await models.User.update_or_create(
            bot_id=bot.id,
            user_id=user.id
        )

        return DbUser(db=db, bot=bot, tg=user, first_interaction=first_interaction)
    
    async def update_session(self, referer: str, time: datetime) -> None:
        if self.first_interaction:
            self.db.referer = referer
            self.db.session_id = 1
            self.db.session_referer = referer
        elif time - self.db.last_action_time > config.SESSION_TIMEOUT:
            self.db.session_id += 1
            self.db.session_referer = referer
        
        self.db.last_action_time = time