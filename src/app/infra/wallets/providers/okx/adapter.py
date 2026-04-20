from datetime import datetime
import time

from app.infra.http import BaseSession
from app.domain.entity import Transaction
from app.application.ports import WalletProvider
from .okx import OKXExchangeClient
from .mapper import to_transaction
from ..utils.key import build_key


class OKXExchangeProvider(WalletProvider):
    def __init__(self, api_key: str, secret: str, passphrase: str, *, external_id: str | None = None, base_url: str = None, client: BaseSession = None):
        self._client = OKXExchangeClient(api_key, secret, passphrase, base_url=base_url)
        self.provider_name = 'OKX'
        self._external_id = external_id or self.provider_name
    
    async def get_transactions(self, wallet_id: int, wallet_external_id: str, start_date: datetime | None, end_date: datetime | None, currency: str = None) -> tuple[Transaction, ...]:
        match wallet_external_id.split(':'):
            case [self.external_id, 'funding']:
                start_ts = int(start_date.timestamp()*1000) if start_date else None
                end_ts = int(end_date.timestamp()*1000) if end_date else int(time.time())
                transactions = await self._client._fetch_all_funding_history(start_ts, end_ts)

                txs = tuple([to_transaction(wallet_id, tx) for tx in transactions])
                return txs
            case [self._external_id, 'spot']:
                start_ts = int(start_date.timestamp()*1000) if start_date else None
                end_ts = int(end_date.timestamp()*1000) if end_date else int(time.time())
                transactions = await self._client._fetch_unified_history(start_ts, end_ts)

                txs = tuple([to_transaction(wallet_id, tx) for tx in transactions.data])
                return txs
            case _:
                return tuple()

    async def get_wallets_ids(self) -> tuple[str, ...]:
        wallets = ("spot", "funding", "earn-simple", "earn-defi")
        return tuple(map(lambda a:build_key(self.external_id, a), wallets))

    @property
    def external_id(self):
        return self._external_id

    async def close(self) -> None:
        return await self._client.close()


