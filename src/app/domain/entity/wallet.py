from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Wallet:
    id: int
    name: str
    account_id: int
    provider_id: str    # UUID hex
    external_id: str    # provider wallet id in format="<provider_name>:<id>" for example: `bybit:SPOT`
    currency: Optional[str] # Default wallet currency; in case None its means wallet is multi-assets[currencies]

    @classmethod
    def create(cls, id: int, name: str, account_id: int, provider_id: str, external_id: str, currency: str = None):

        return Wallet(
            id=id,
            name=name,
            account_id=account_id,
            provider_id=provider_id,
            external_id=external_id,
            currency=currency
        )

