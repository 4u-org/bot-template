import asyncio
from typing import Awaitable, TypeVar

_T = TypeVar("_T")

async def wait(coro: Awaitable[_T]) -> _T:
    return await coro

def start(coro: Awaitable[_T]) -> asyncio.Task[_T]:
    return asyncio.create_task(wait(coro))