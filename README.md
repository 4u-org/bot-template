# Telegram bot template

## Hot reload (Update on save)
to use hot reload run bot with
```
reloadium run run.py
```
more info: https://github.com/reloadware/reloadium

## Translations
create locales folder:  
```
mkdir locales
```
init or update extracted texts:  
```
pybabel extract --input-dirs=. --ignore venv -k __:1,2 -o locales/messages.pot
```
add language:  
```
pybabel init -i locales/messages.pot -d locales -D messages -l en
```
update all languages:  
```
pybabel update -d locales -D messages -i locales/messages.pot
```
more info: https://docs.aiogram.dev/en/dev-3.x/utils/i18n.html  
translations are compiled automatically on startup  

## Migrations
init migrations:  
```
aerich init -t db.database.TORTOISE_ORM
aerich init-db
```
commit changes:  
```
aerich migrate --name drop_column
```
apply changes:  
```
aerich upgrade
```
more info: https://github.com/tortoise/aerich  
Migrations are applied automatically on startup if LOCAL=False  

