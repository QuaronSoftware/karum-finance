from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.application.ports import UoWFactory

from .repositorys import (
    AccountRepositoryORM,
    WalletRepositoryORM,
    TransactionRepositoryORM,
)


@dataclass
class UoW(UoWFactory):
    session_factory: async_sessionmaker[AsyncSession]

    session: AsyncSession | None = None
    accounts: AccountRepositoryORM | None = None
    wallets: WalletRepositoryORM | None = None
    transactions: TransactionRepositoryORM | None = None

    async def __aenter__(self) -> "UoW":
        self.session = self.session_factory()
        self.accounts = AccountRepositoryORM(self.session)
        self.wallets = WalletRepositoryORM(self.session)
        self.transactions = TransactionRepositoryORM(self.session)

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

