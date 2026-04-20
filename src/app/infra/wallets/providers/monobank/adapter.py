import time
from datetime import datetime

from app.application.ports import WalletProvider
from app.domain.entity import Transaction
from .mapper import to_transaction
from .monobank import MonobankClient, CURRENCY_MAP


class MonobankProvider(WalletProvider):
    def __init__(self, api_key: str, *, external_id: str | None = None, base_url: str = None):
        self._client = MonobankClient(api_key, base_url=base_url)
        self.provider_name = 'Monobank'
        self._external_id = external_id or self.provider_name
        self.default_currency = "UAH"
    
    async def get_transactions(self, wallet_id: int, wallet_external_id: str, start_date: datetime | None, end_date: datetime | None, currency: str = None) -> tuple[Transaction, ...]:
        start_ts = int(start_date.timestamp()) if start_date else None
        end_ts = int(end_date.timestamp()) if end_date else int(time.time())
        transactions = await self._client._get_transactions(wallet_external_id, start_ts, end_ts)

        txs = tuple([to_transaction(wallet_id, tx, currency or CURRENCY_MAP[tx.currencyCode]) for tx in transactions])
        return txs
    
    async def get_wallets_ids(self) -> tuple[str, ...]:
        accounts = await self._client._fetch_client_info()
        return tuple(a.id for a in accounts)
    
    @property
    def external_id(self):
        return self._external_id

    async def close(self) -> None:
        return await self._client.close()
