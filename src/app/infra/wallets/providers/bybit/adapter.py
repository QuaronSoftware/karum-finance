import time
from datetime import datetime

from app.application.ports import WalletProvider
from app.domain.entity import Transaction
from .bybit import ByBitExchangeClient
from .mapper import to_transaction
from ..utils.key import build_key


class ByBitExchangeProvider(WalletProvider):
    def __init__(self, api_key: str, secret: str, *, external_id: str | None = None, base_url: str = None):
        self._client = ByBitExchangeClient(api_key, secret, base_url=base_url)

        self.provider_name = 'ByBit'
        self._external_id = external_id or self.provider_name
    
    async def get_transactions(self, wallet_id: int, wallet_external_id: str, start_date: datetime | None, end_date: datetime | None, currency: str = None) -> tuple[Transaction, ...]:

        match wallet_external_id.split(':'):
            case [self.external_id, 'UNIFIED']:
                start_ts = int(start_date.timestamp()) if start_date else None
                end_ts = int(end_date.timestamp()) if end_date else int(time.time())
                transactions = await self._client._fetch_transactions(start_ts, end_ts)

                txs = tuple([to_transaction(wallet_id, tx) for tx in transactions])
                return txs
            case _:
                return tuple()

    async def get_wallets_ids(self) -> tuple[str, ...]:
        wallets = self._client.get_account_wallets_names()
        return tuple(map(lambda a:build_key(self.external_id, a), wallets))

    @property
    def external_id(self):
        return self._external_id

    async def close(self) -> None:
        return await self._client.close()
