from web.utils import Routes
from web.webapp import inline_demo, reply_demo

routes = Routes("/webapp")
routes.add_routes(inline_demo.routes)
routes.add_routes(reply_demo.routes)