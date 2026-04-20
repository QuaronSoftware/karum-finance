from datetime import datetime
from dataclasses import dataclass
from typing import Literal
from .currency import Currency, BaseCurrencyCode, BASE_CURRENCIES

AccountType = Literal['personal', 'business']


@dataclass(frozen=True)
class Account:
    id: int
    name: str
    currency: Currency
    owner_id: int
    type: AccountType
    date_added: datetime

    @classmethod
    def create(cls,
               id: int,
               name: str,
               currency: Currency | BaseCurrencyCode,
               owner_id: int,
               type: AccountType,
               date_added: datetime
    ):
        # Input validation
        if isinstance(currency, BaseCurrencyCode):
            currency = BASE_CURRENCIES[currency]

        return Account(
            id=id,
            name=name,
            currency=currency,
            owner_id=owner_id,
            type=type,
            date_added=date_added
        )
