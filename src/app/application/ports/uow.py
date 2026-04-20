from typing import Protocol
from ..ports.repositories import (
    AccountRepository,
    WalletRepository,
    TransactionRepository
)


class UoWFactory(Protocol):
    async def __aenter__(self) -> "UoW": ...
    async def __aexit__(self, exc_type, exc, tb): ...

class UoW(Protocol):
    accounts: AccountRepository
    wallets: WalletRepository
    transactions: TransactionRepository
