from __future__ import annotations
from tortoise.models import Model
from tortoise import fields

class Bot(Model):
    class Meta:
        table="bots"
    id = fields.BigIntField(pk=True)
    token = fields.CharField(max_length=50)
    # default_language_code = fields.CharField(max_length=2)

class User(Model):
    class Meta:
        table="users"
        unique_together = (("bot", "user_id"), )

    # Default tg user params

    # Telegram bot (if this script is used to run multiple bots)
    bot: fields.ForeignKeyRelation[Bot] = fields.ForeignKeyField('models.Bot')
    # Telegram user id
    user_id = fields.BigIntField()

    # Default additional params

    # Can bot write to this user via private messages
    can_write = fields.BooleanField(default=False)
    # When user was added into database
    first_action_time = fields.DatetimeField(auto_now_add=True)
    # When user made his last interaction with bot
    last_action_time = fields.DatetimeField(auto_now_add=True)
    # Who invited this user (more info in notion)
    referer = fields.CharField(max_length=64, default=None, null=True)
    # Session is a secuence of actions that are less then 5 minutes apart (more info in notion)
    session_id = fields.IntField(default=0)
    # Who invited this user to reuse the bot (more info in notion)
    session_referer = fields.CharField(max_length=64, default=None, null=True)
    # What content id is the user exploring right now
    # content_id = fields.IntField(default=None)
    # Who invited this user to explore this content (more info in notion)
    # content_referer_id = fields.BigIntField(default=None)
    pm_referer = fields.CharField(max_length=64, default=None, null=True)

    # Custom params

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return f"[User {self.user_id}]"

class TgUser(Model):
    class Meta:
        table = "tgusers"

    # Telegram user id
    user_id = fields.BigIntField(pk=True)
    # Telegram user name
    first_name = fields.CharField(max_length=64) # Group and channel max: 255
    # Telegram user last name
    last_name = fields.CharField(max_length=64, null=True)
    # Telegram user username
    username = fields.CharField(max_length=32, index=True, null=True)
    # Telegram language code
    language_code = fields.CharField(max_length=2, null=True)
    # True, if this user is a Telegram Premium user
    is_premium = fields.BooleanField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)