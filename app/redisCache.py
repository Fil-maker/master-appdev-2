# app/core/cache.py
import json
from typing import Any, Optional

from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis_url: str = "redis://217.76.176.93:6379"):
        self.redis_url = redis_url
        self.client: Optional[Redis] = None

    async def connect(self):
        """Подключение к Redis"""
        self.client = Redis.from_url(self.redis_url, decode_responses=True)

    async def disconnect(self):
        """Отключение от Redis"""
        if self.client:
            await self.client.aclose()

    async def get(self, key: str) -> Optional[Any]:
        """Получение данных из кэша"""
        if not self.client:
            return None

        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(
            self,
            key: str,
            value: Any,
            ttl: int = 60 * 10
    ) -> None:
        """Сохранение данных в кэш с TTL"""
        if self.client:
            await self.client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )

    async def delete(self, key: str) -> None:
        """Удаление данных из кэша"""
        if self.client:
            await self.client.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        """Удаление по шаблону"""
        if self.client:
            keys = await self.client.keys(pattern)
            if keys:
                await self.client.delete(*keys)

    async def invalidate_cache(self, cache_key: str) -> None:
        """Инвалидация кэша"""
        await self.delete(cache_key)
