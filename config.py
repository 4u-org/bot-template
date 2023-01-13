from datetime import timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Used in session_middleware, defines how long stats session can wait until reset
SESSION_TIMEOUT = timedelta(seconds=int(getenv("SESSION_TIMEOUT", 60*5)))

LOCAL = getenv("LOCAL", "True").lower() in ['true', '1']
TOKEN = getenv("TELEGRAM_TOKEN")

DATABASE_URL = getenv("DATABASE_URL").replace("postgresql://", "postgres://")

if LOCAL:
    WEB_SERVER_HOST = getenv("WEB_SERVER_HOST", "127.0.0.1")
    WEB_SERVER_PORT = int(getenv("WEB_SERVER_PORT", 8000))
    BASE_URL = getenv("BASE_URL", f"https://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
else:
    WEB_SERVER_HOST = getenv("WEB_SERVER_HOST")
    WEB_SERVER_PORT = int(getenv("WEB_SERVER_PORT", 8000))
    BASE_URL = getenv("BASE_URL", "https://" + WEB_SERVER_HOST)
    MAIN_BOT_PATH = "/webhook/main"
    OTHER_BOTS_PATH = "/webhook/bot/{bot_token}"
    REDIS_URL = getenv("REDIS_URL")