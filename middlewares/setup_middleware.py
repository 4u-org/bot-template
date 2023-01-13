from aiogram import BaseMiddleware, Router
from typing import Optional, Set

class SetupMiddleware(BaseMiddleware):
    def setup(
        self: BaseMiddleware, router: Router, exclude: Optional[Set[str]] = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {"update", "error", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self