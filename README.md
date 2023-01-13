# Telegram bot template

init or update extracted texts:
`pybabel extract --input-dirs=. --ignore venv -o locales/messages.pot`
add language:
`pybabel init -i locales/messages.pot -d locales -D messages -l en`
update all languages:
`pybabel update -d locales -D messages -i locales/messages.pot`
more info: https://docs.aiogram.dev/en/dev-3.x/utils/i18n.html
translations are compiled automatically on startup

init migrations:
```
aerich init -t db.database.TORTOISE_ORM
aerich init-db
```
commit changes:
`aerich migrate --name drop_column`
apply changes:
`aerich upgrade`
more info: https://github.com/tortoise/aerich
migrations are applied automatically on startup

