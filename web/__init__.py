from aiohttp import web
from web import webapp
from web.utils import Routes

routes = Routes()
routes.add_routes(webapp.routes)