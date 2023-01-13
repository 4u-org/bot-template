from aiohttp import web
from web import webapp

router = web.UrlDispatcher()
router.add_routes(webapp.routes)