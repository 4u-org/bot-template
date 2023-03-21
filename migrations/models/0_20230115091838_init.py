from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "bots" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "tgusers" (
    "user_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(64) NOT NULL,
    "last_name" VARCHAR(64),
    "username" VARCHAR(32),
    "language_code" VARCHAR(2),
    "is_premium" BOOL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_tgusers_usernam_9bce32" ON "tgusers" ("username");
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "can_write" BOOL NOT NULL  DEFAULT False,
    "first_action_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_action_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "referer_id" BIGINT,
    "session_id" INT NOT NULL  DEFAULT 0,
    "session_referer_id" BIGINT,
    "bot_id" BIGINT NOT NULL REFERENCES "bots" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_users_bot_id_bec2bb" UNIQUE ("bot_id", "user_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
