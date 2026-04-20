from decimal import Decimal

from pydantic import BaseModel
from decimal import Decimal
from typing import Dict
from karum.application.ports import PriceProvider
from karum.infra.http import AiohttpSession,  BaseSession


class RateResponse(BaseModel):
    amount: int
    base: str
    rates: Dict[str,  Decimal]

class UniRatePriceProvider(PriceProvider):
    def __init__(self, base_currency: str,  api_key: str, *,  base_url: str = None,  client: BaseSession = None) -> None:
        self._rates: Dict[str,  Decimal] = {}
        self._client = client or AiohttpSession(base_url)
        self._api_key = api_key
        self._base_currency = base_currency
    
    async def _fetch_rates(self):
        path = '/api/rates'
        params = {
            'api_key': self._api_key, 
            'amount': '1', 
            'from': self._base_currency, 
            'format': 'json', 
        }
        try:
            resp = await self._client.make_request(path,  params=params,  response_model=RateResponse)
            self._rates.update(resp.rates)
        except Exception:
            return False

        return True

    @property
    def currency(self):
        return self._base_currency
    
    @property
    def rates(self) -> Dict[str, Decimal]:
        return self._rates
    
    async def get_rate(self, currency: str) -> Decimal:
        ok = await self._fetch_rates()
        if ok and (rate := self.rates.get(currency)):
            return rate
        return Decimal('0')

    async def close(self) -> None:
        return await self._client.close()
