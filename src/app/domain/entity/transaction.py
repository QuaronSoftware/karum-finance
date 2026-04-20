from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import Literal, Optional
from .asset import Asset
from .category import Category

TransactionType = Literal['income', 'expense', 'transfer', 'swap']


@dataclass(frozen=True)
class Transaction:
    id: int
    type: TransactionType
    asset: Optional[Asset]
    from_asset: Optional[Asset]
    to_asset: Optional[Asset]
    note: Optional[str]
    category: Optional[Category]
    from_wallet_id: int
    to_wallet_id: int
    external_id: str    # transaction id in provider.
    occurred_at: datetime

    @classmethod
    def new_income(cls,
                    id: int,
                    amount: Decimal,
                    symbol: str,
                    wallet_id: int,
                    occurred_at: datetime,
                    external_id: str,
                    category: str | Category | None,
                    note: str | None = None
    ):
        asset = Asset.create(symbol, amount)

        return Transaction(
            id=id,
            type='income',
            asset=asset,
            to_asset=None,
            from_asset=None,
            note=note,
            category=category,
            to_wallet_id=wallet_id,
            from_wallet_id=None,
            external_id=external_id,
            occurred_at=occurred_at
        )

    @classmethod
    def new_expense(cls,
                    id: int,
                    amount: Decimal,
                    symbol: str,
                    wallet_id: int,
                    occurred_at: datetime,
                    external_id: str,
                    category: str | Category | None,
                    note: str | None = None
    ):
        asset = Asset.create(symbol, amount)

        return Transaction(
            id=id,
            type='expense',
            asset=asset,
            to_asset=None,
            from_asset=None,
            note=note,
            category=category,
            to_wallet_id=None,
            from_wallet_id=wallet_id,
            external_id=external_id,
            occurred_at=occurred_at
        )
    
    @classmethod
    def new_transfer(cls,
                     id: int,
                     amount: Decimal,
                     symbol: str,
                     from_wallet_id: int,
                     to_wallet_id: int,
                     occurred_at: datetime,
                     external_id: str,
                     category: str | Category | None,
                     note: str | None = None
    ):
        asset = Asset.create(symbol, amount)

        return Transaction(
            id=id,
            type='transfer',
            asset=asset,
            to_asset=None,
            from_asset=None,
            note=note,
            category=category,
            to_wallet_id=to_wallet_id,
            from_wallet_id=from_wallet_id,
            external_id=external_id,
            occurred_at=occurred_at
        )
    
    @classmethod
    def new_swap(cls,
                 id: int,
                 to_amount: Decimal,
                 from_amount: Decimal,
                 to_symbol: str,
                 from_symbol: str,
                 from_wallet_id: int,
                 to_wallet_id: int,
                 occurred_at: datetime,
                 external_id: str,
                 category: str | Category | None,
                 note: str | None = None
    ):
        from_asset = Asset.create(from_symbol, from_amount)
        to_asset = Asset.create(to_symbol, to_amount)

        return Transaction(
            id=id,
            type='swap',
            asset=None,
            to_asset=to_asset,
            from_asset=from_asset,
            note=note,
            category=category,
            to_wallet_id=to_wallet_id,
            from_wallet_id=from_wallet_id,
            external_id=external_id,
            occurred_at=occurred_at
        )
    
    @classmethod
    def create(cls,
               id: int,
               type: TransactionType,
               amount: Decimal = None,
               symbol: str = None,
               wallet_id: int = None,
               to_amount: Decimal = None,
               from_amount: Decimal = None,
               to_symbol: str = None,
               from_symbol: str = None,
               from_wallet_id: int = None,
               to_wallet_id: int = None,
               external_id: str = None,
               category: str | Category | None = None,
               note: str | None = None,
               occurred_at: datetime = None,
    ):
        match type:
            case 'income':
                return cls.new_income(
                    id=id,
                    amount=amount,
                    symbol=symbol,
                    wallet_id=wallet_id,
                    category=category,
                    note=note,
                    external_id=external_id,
                    occurred_at=occurred_at
                )
            case 'expense':
                return cls.new_expense(
                    id=id,
                    amount=amount,
                    symbol=symbol,
                    wallet_id=wallet_id,
                    category=category,
                    note=note,
                    external_id=external_id,
                    occurred_at=occurred_at
                )
            case 'transfer':
                return cls.new_transfer(
                    id=id,
                    amount=amount,
                    symbol=symbol,
                    from_wallet_id=from_wallet_id,
                    to_wallet_id=to_wallet_id,
                    category=category,
                    note=note,
                    external_id=external_id,
                    occurred_at=occurred_at
                )
            case 'swap':
                return cls.new_swap(
                    id=id,
                    to_amount=to_amount,
                    from_amount=from_amount,
                    to_symbol=to_symbol,
                    from_symbol=from_symbol,
                    from_wallet_id=from_wallet_id,
                    to_wallet_id=to_wallet_id,
                    category=category,
                    note=note,
                    external_id=external_id,
                    occurred_at=occurred_at
                )

