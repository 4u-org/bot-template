from __future__ import annotations
from aiogram import types, Bot
from datetime import datetime

from db import models
import config as cnf

class DbUser(types.User):
    first_interaction: bool
    db: models.User
    bot: Bot

    class Config:
        arbitrary_types_allowed = True
    
    async def create(user: types.User, bot: Bot) -> DbUser:
        db, first_interaction = await models.User.update_or_create(
            bot_id=bot.id,
            user_id=user.id
        )
        
        data = user.dict()
        data["bot"] = bot
        data["db"] = db
        data["first_interaction"] = first_interaction

        return DbUser(**data)
    
    async def update_session(self, referer: int, time: datetime) -> None:
        if self.first_interaction:
            self.db.referer_id = referer
            self.db.session_id = 1
            self.db.session_referer_id = referer
        elif time - self.db.last_action_time > cnf.SESSION_TIMEOUT:
            self.db.session_id += 1
            self.db.session_referer_id = referer
        
        self.db.last_action_time = time