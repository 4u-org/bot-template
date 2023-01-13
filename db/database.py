from tortoise import Tortoise
from aerich import Command
import config as cfg

TORTOISE_ORM = {
    "connections": {"default": cfg.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init():
    await Tortoise.init(TORTOISE_ORM)

async def close():
    await Tortoise.close_connections()

async def migrate():
    command = Command(tortoise_config=TORTOISE_ORM)
    await command.init()
    await command.upgrade()