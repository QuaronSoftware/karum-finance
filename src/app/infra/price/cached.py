from decimal import Decimal

from app.application.ports import PriceProvider, Cache


class CachePriceProvider(PriceProvider):
    def __init__(self, inner: PriceProvider, cache: Cache, ttl: int = 480):
        self._inner = inner
        self._cache = cache
        self.ttl = ttl

    def _key(self, base: str):
        return f'rate:{base}'

    @property
    def currency(self):
        return self._inner.currency

    @property
    def rates(self):
        return self._inner.rates

    async def get_rate(self, currency: str) -> Decimal:
        key = self._key(self._inner.currency)

        # Get cached rates if exists
        cached = await self._cache.get(key)
        if isinstance(cached, dict) and currency in cached:
            return cached[currency]
        
        # Fetch new rates and cache
        val = await self._inner.get_rate(currency)
        await self._cache.set(key, self.rates, self.ttl)
        return val
    
    def close(self):
        return self._inner.close()

