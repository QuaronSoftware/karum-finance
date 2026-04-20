from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel
from app.domain.entity import TransactionType

class OverviewAssetShortDTO(BaseModel):
    symbol: str
    amount: Decimal
    ac: Optional[Decimal]   # Amount in :currency:
    rate: Optional[Decimal]    # Price 1 symbol in :currency:

class OverviewAssetDTO(OverviewAssetShortDTO):
    buy_price: Optional[Decimal]

class OverviewWalletDTO(BaseModel):
    wallet_provider_name: str
    wallet_name: str
    assets: List[OverviewAssetDTO]
    total_amount: Decimal

class OverviewTransactionDTO(BaseModel):
    wallet_name: str
    amount: Decimal
    type: TransactionType
    occurred_at: datetime

class OverviewDTO(BaseModel):
    tac: Decimal    # Total amount in :currency:
    currency: str   # System currency
    tx_count: int   # Total transactions count
    wallets: List[OverviewWalletDTO]
    assets: List[OverviewAssetShortDTO]
    last_tx: List[OverviewTransactionDTO]   # Show last N transactions
