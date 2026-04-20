from datetime import datetime
from typing import Tuple
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from karum.application.ports.repositories import AccountRepository
from karum.domain.enum import BaseCurrencyCode
from karum.domain.entity import Account, BASE_CURRENCIES
from karum.infra.db.models import AccountORM


class AccountRepositoryORM(AccountRepository):

    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: AccountORM):
        if model is None: return None
        return Account.create(
            id=model.id,
            name=model.name,
            currency=model.currency,
            owner_id=model.owner_id,
            type=model.type,
            date_added=datetime.fromtimestamp(model.date_added)
        )

    async def create(self, account: Account):
        # model
        model = AccountORM(
            name=account.name,
            type=account.type,
            owner_id=account.owner_id,
            currency=account.currency.code,
            date_added=int(account.date_added.timestamp())
        )
        # add and commit
        self.session.add(model)
        await self.session.commit()

        return self._to_domain(model)

    async def get(self, id: str) -> Account:

        # query
        query = select(AccountORM).where(AccountORM.id==id)
        result = await self.session.execute(query)

        # return repsonse
        return self._to_domain(result.scalar())

    async def get_all(self) -> Tuple[Account, ...]:
        # query
        query = select(AccountORM)
        result = await self.session.execute(query)

        # return repsonse
        return tuple(map(self._to_domain, result.scalars().all()))

    async def update(self, id: str, data: dict = {}, **kwargs):
        await self.session.execute(
            update(AccountORM).where(AccountORM.id == id).values(data | kwargs)
        )

    async def delete(self, id: int) -> bool:
        query = delete(AccountORM).where(AccountORM.id==id)
        await self.session.execute(query)

        return True
