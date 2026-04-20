import asyncio
from decimal import Decimal

from app.infra.http import AiohttpSession, BaseSession
from .models import MonobankPersonalInfo, MonobankAccount, MonobankListTransaction


CURRENCY_MAP = {
    980: "UAH",
    840: "USD",
    978: "EUR",
    826: "GBP",
    392: "JPY",
    756: "CHF",
    985: "PLN",
    203: "CZK",
    348: "HUF",
    949: "TRY",
    124: "CAD",
    36: "AUD",
}
TRANSACTION_TIME_RANGE = 2_678_400  # 31 days


class MonobankClient:
    def __init__(self, api_key: str, *, base_url: str = None, client: BaseSession = None):
        self._client = client or AiohttpSession(base_url)
        self._api_key = api_key
    
    def _build_headers(self):
        return {
            'X-Token': self._api_key,
            'Content-Type': 'application/json'
        }
    
    async def _fetch_client_info(self) -> list[MonobankAccount]:
        path = '/personal/client-info'
        headers = self._build_headers()

        resp = await self._client.make_request(path, headers=headers, response_model=MonobankPersonalInfo)
    
        return resp.accounts

    async def get_account_balances(self) -> tuple:
        assets = await self._fetch_client_info()
        data = tuple(
            ((CURRENCY_MAP.get(acc.currencyCode), balance, 0), acc.id)
            for acc in assets
            if (balance := Decimal(acc.balance)/100) > 0
        )
        """wallets = tuple(
            to_wallet(id, tuple([assets]), 'fiat', provider=self.provider_name)
            for assets, id in data
        )"""
        return data

    async def _fetch_transactions(self, wallet_id: int, start_date: int, end_date: int) -> MonobankListTransaction:
        path = f"/personal/statement/{wallet_id}/{start_date or ''}/{end_date or ''}"
        headers = self._build_headers()

        resp = await self._client.make_request(path, headers=headers, response_model=MonobankListTransaction)
    
        return list(resp)
    
    async def _get_transaction_window(self, wallet_id: int, start_date: int, end_date: int):
        
        end_date = start_date+TRANSACTION_TIME_RANGE if end_date or (end_date-start_date)>TRANSACTION_TIME_RANGE else end_date
        return await self._fetch_transactions(wallet_id, start_date, end_date)
    
    async def _get_transactions(self, wallet_id: int, start_date: int, end_date: int) -> MonobankListTransaction:
        all_transactions = []
        current_from = start_date

        while current_from < end_date:
            current_to = min(current_from + TRANSACTION_TIME_RANGE, end_date)

            chunk = await self._get_transaction_window(wallet_id, current_from, current_to)
            all_transactions.extend(chunk)
            await asyncio.sleep(2)

            current_from = current_to

        return all_transactions

    async def close(self) -> None:
        return await self._client.close()
