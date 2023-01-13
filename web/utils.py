from __future__ import annotations
from os import PathLike
from typing import Any
from aiohttp.web import RouteTableDef, RouteDef, StaticDef

def prefix_route(prefix: str, route):
    dict = {}

    if isinstance(route, StaticDef):
        dict["prefix"] = prefix + route.prefix
        dict["path"] = route.path
        dict["kwargs"] = route.kwargs
        return StaticDef(**dict)
    elif isinstance(route, RouteDef):
        dict["method"] = route.method
        dict["path"] = prefix + route.path
        dict["handler"] = route.handler
        dict["kwargs"] = route.kwargs
        return RouteDef(**dict)

class Routes(RouteTableDef):
    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        super().__init__()

    def add_routes(self, routes: Routes):
        for route in routes:
            route_copy = prefix_route(self.prefix, route)
            self._items.append(route_copy)

    def route(self, method: str, path: str, **kwargs: Any):
        path = self.prefix + path
        return super().route(method, path, **kwargs)

    def static(self, prefix: str, path: PathLike, **kwargs: Any) -> None:
        prefix = self.prefix + prefix
        return super().static(prefix, path, **kwargs)