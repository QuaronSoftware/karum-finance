import asyncio
import time
from typing import Any

from app.application.ports import Cache



class TTLMemoryCache(Cache):
    def __init__(self) -> None:
        self._data: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any | None:
        item = self._data.get(key)
        if item is None:
            return None

        value, expires_at = item

        if expires_at < time.monotonic():
            # expired → clean
            self._data.pop(key, None)
            return None

        return value

    async def set(self, key: str, value: Any, ttl: float) -> None:
        expires_at = time.monotonic() + ttl

        async with self._lock:
            self._data[key] = (value, expires_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._data.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._data.clear()