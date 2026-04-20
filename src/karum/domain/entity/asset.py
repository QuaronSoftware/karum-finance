from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Asset:
    symbol: str
    amount: Decimal

    @classmethod
    def create(cls, symbol: str, amount: str | int | Decimal):
        # Input validation
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Amount cannot be negotive")
        if not symbol:
            raise ValueError("Argument \"symbol\" cannot be empty")
        
        return Asset(
            symbol=symbol,
            amount=amount
        )


@dataclass(frozen=True)
class AssetPosition(Asset):
    avarage_price_buy: Decimal

    @classmethod
    def create(cls, avarage_price_buy: str | int | Decimal, symbol: str, amount: str | int | Decimal):
        # Input validation
        if amount is None: 
            raise ValueError("Argument \"amount\" cannot be empty")
        if not symbol:
            raise ValueError("Argument \"symbol\" cannot be None or empty")
        if avarage_price_buy is None: 
            raise ValueError("Argument \"avarage_price_buy\" cannot be empty")
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
        if not isinstance(avarage_price_buy, Decimal):
            avarage_price_buy = Decimal(avarage_price_buy)
        
        return AssetPosition(
            symbol=symbol,
            amount=amount,
            avarage_price_buy=avarage_price_buy
        )
