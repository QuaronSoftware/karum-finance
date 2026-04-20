import time
from typing import Tuple
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import WalletRepository
from app.domain.entity import Wallet
from app.infra.db.models import WalletORM


class WalletRepositoryORM(WalletRepository):

    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: WalletORM):
        if model is None: return None
        return Wallet.create(
            id=model.id,
            name=model.name,
            account_id=model.account_id,
            provider_id=model.provider_id,
            external_id=model.external_id,
            currency=model.currency
        )

    async def create(self, wallet: Wallet):
        query = select(WalletORM).where(WalletORM.provider_id==wallet.provider_id, WalletORM.external_id==wallet.external_id)
        resp = await self.session.execute(query)
        model = resp.scalar()
        if not model:
            # model
            model = WalletORM(
                name=wallet.name,
                account_id=wallet.account_id,
                provider_id=wallet.provider_id,
                external_id=wallet.external_id,
                currency=wallet.currency,
                date_added=int(time.time())
            )
            # add and commit
            self.session.add(model)
            await self.session.commit()

        return self._to_domain(model)

    async def get(self, id: str) -> Wallet:

        # query
        query = select(WalletORM).where(WalletORM.id==id)
        result = await self.session.execute(query)

        # return repsonse
        return self._to_domain(result.scalar())

    async def get_all(self, account_id: int) -> Tuple[Wallet, ...]:
        # query
        query = select(WalletORM).where(WalletORM.account_id==account_id)
        result = await self.session.execute(query)

        # return repsonse
        return tuple(map(self._to_domain, result.scalars().all()))
    
    async def get_all_by_provider_id(self, provider_id: str) -> Tuple[Wallet, ...]:
        # query
        query = select(WalletORM).where(WalletORM.provider_id==provider_id)
        result = await self.session.execute(query)

        # return repsonse
        return tuple(map(self._to_domain, result.scalars().all()))

    async def update(self, id: str, data: dict = {}, **kwargs):
        await self.session.execute(
            update(WalletORM).where(WalletORM.id == id).values(data | kwargs)
        )

