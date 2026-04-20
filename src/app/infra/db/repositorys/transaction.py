from datetime import datetime
from typing import Tuple
from sqlalchemy import select, update, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import TransactionRepository
from app.domain.entity import Transaction, TransactionType
from app.domain.entity.category import Category
from app.infra.db.models import TransactionORM
from app.shared.debug import track_time


class TransactionRepositoryORM(TransactionRepository):

    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: TransactionORM):
        if model is None: return None
        return Transaction.create(
            id=model.id,
            type=model.type,
            amount=model.amount,
            symbol=model.asset,
            wallet_id=model.wallet_id,
            to_amount=model.to_amount,
            from_amount=model.from_amount,
            to_symbol=model.to_asset,
            from_symbol=model.from_asset,
            from_wallet_id=model.from_wallet_id,
            to_wallet_id=model.to_wallet_id,
            category=model.category_id,
            note=model.note,
            external_id=model.external_id,
            occurred_at=datetime.fromtimestamp(model.occurred_at)
        )
    
    async def create(self, tx: Transaction) -> Transaction:
        # Validate unique external id # TODO

        # Create and add object
        model = TransactionORM(
            type=tx.type,
            amount=tx.asset.amount if tx.asset else None,
            asset=tx.asset.symbol if tx.asset else None,
            wallet_id=tx.to_wallet_id, # check
            from_asset=tx.from_asset.symbol if tx.from_asset else None,
            from_amount=tx.from_asset.amount if tx.from_asset else None,
            from_wallet_id=tx.from_wallet_id,
            to_asset=tx.to_asset.symbol if tx.to_asset else None,
            to_amount=tx.to_asset.amount if tx.to_asset else None,
            to_wallet_id=tx.to_wallet_id,
            note=tx.note,
            external_id=tx.external_id,
            category_id=tx.category.id if tx.category else None,
            occurred_at=int(tx.occurred_at.timestamp())
        )
        self.session.add(model)
        await self.session.commit()
        
        # Map to domain then return
        return self._to_domain(model)
    
    async def create_many(self, txs: list[Transaction]) -> tuple[Transaction, ...]:
        res = []

        for tx in txs:
            # Create and add object
            model = TransactionORM(
                type=tx.type,
                amount=tx.asset.amount if tx.asset else None,
                asset=tx.asset.symbol if tx.asset else None,
                wallet_id=tx.to_wallet_id, # check
                from_asset=tx.from_asset.symbol if tx.from_asset else None,
                from_amount=tx.from_asset.amount if tx.from_asset else None,
                from_wallet_id=tx.from_wallet_id,
                to_asset=tx.to_asset.symbol if tx.to_asset else None,
                to_amount=tx.to_asset.amount if tx.to_asset else None,
                to_wallet_id=tx.to_wallet_id,
                note=tx.note,
                external_id=tx.external_id,
                category_id=tx.category.id if tx.category else None,
                occurred_at=int(tx.occurred_at.timestamp())
            )
            self.session.add(model)
            res.append(model)
        
        # Commit
        await self.session.commit()

        # Map response list to domains then return
        return tuple(map(self._to_domain, res))
    
    async def get(self, id: int) -> Transaction:
        # Fetch transaction by id
        query = select(TransactionORM).where(TransactionORM.id==id)
        resp = await self.session.execute(query)

        # Map to domain then return
        return self._to_domain(resp.scalar())
    
    async def get_last(self, wallet_id: int) -> Transaction:
        # Fetch transaction by type
        query = select(TransactionORM).where(
            or_(TransactionORM.wallet_id==wallet_id,
                TransactionORM.from_wallet_id==wallet_id,
                TransactionORM.to_wallet_id==wallet_id
            )
        ).order_by(TransactionORM.occurred_at.desc()).limit(1)
        resp = await self.session.execute(query)

        # Map to domain then return
        return self._to_domain(resp.scalar())
    
    async def get_all_by_type(self, wallet_id: int, type: TransactionType, start_date: int, end_date: int, page: int = 0, limit: int = None) -> Tuple[Transaction, ...]:
        # Fetch transaction by type
        query = select(TransactionORM).where(
            TransactionORM.type==type,
            or_(TransactionORM.wallet_id==wallet_id,
                TransactionORM.from_wallet_id==wallet_id,
                TransactionORM.to_wallet_id==wallet_id
            )
        )

        # Pagging
        if start_date is not None:
            query = query.where(TransactionORM.occurred_at>=start_date)
        if end_date is not None:
            query = query.where(TransactionORM.occurred_at<=end_date)
        if page is not None and limit is not None:
            query = query.offset(page * limit)
        if limit is not None:
            query = query.limit(limit)

        resp = await self.session.execute(query)

        # Map response list to domains then return
        return tuple(map(self._to_domain, resp.scalars().all()))
    
    async def get_all(self, wallet_id: int, start_date: int, end_date: int, page: int = 0, limit: int = None) -> Tuple[Transaction, ...]:
        # Fetch transaction by type
        query = select(TransactionORM).where(
            or_(TransactionORM.wallet_id==wallet_id,
                TransactionORM.from_wallet_id==wallet_id,
                TransactionORM.to_wallet_id==wallet_id
            )
        )

        # Pagging
        if start_date is not None:
            query = query.where(TransactionORM.occurred_at>=start_date)
        if end_date is not None:
            query = query.where(TransactionORM.occurred_at<=end_date)
        if page is not None and limit is not None:
            query = query.offset(page * limit)
        if limit is not None:
            query = query.limit(limit)

        resp = await self.session.execute(query)

        # Map response list to domains then return
        return tuple(map(self._to_domain, resp.scalars().all()))
    
    async def update_category(self, tx_id: int, category: Category) -> None:
        query = update(TransactionORM).where(TransactionORM.id==tx_id).values(category_id=category.id)
        await self.session.execute(query)

    async def count(self, wallet_id: int) -> int:
        query = select(func.count()).where(
            or_(TransactionORM.wallet_id==wallet_id,
                TransactionORM.from_wallet_id==wallet_id,
                TransactionORM.to_wallet_id==wallet_id
            )
        )
        resp = await self.session.execute(query)

        # Return response or 0 in other case
        return resp.scalar() or 0
        
