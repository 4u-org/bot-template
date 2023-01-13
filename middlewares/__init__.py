from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from middlewares.db_middleware import DbMiddleware
from middlewares.referer_middleware import SimpleRefererMiddleware
from middlewares.session_middleware import SessionMiddleware

i18n = FSMI18nMiddleware(I18n(path="locales", default_locale="en", domain="messages"))

db = DbMiddleware()
referer = SimpleRefererMiddleware()
session = SessionMiddleware()