from decimal import Decimal
from datetime import datetime

from app.domain.entity import Transaction
from .models import MonobankTransaction


def to_transaction(wallet_id: str, tx: MonobankTransaction, currency: str) -> Transaction:
    if tx.amount >= 0:
        return Transaction.new_income(
            id=None,
            amount=Decimal(abs(tx.amount))/Decimal(100),
            symbol=currency,
            wallet_id=wallet_id,
            note=tx.comment or tx.description,
            occurred_at=datetime.fromtimestamp(tx.time),
            external_id=tx.id,
            category=None
        )
    return Transaction.new_expense(
        id=None,
        amount=Decimal(abs(tx.amount))/Decimal(100),
        symbol=currency,
        wallet_id=wallet_id,
        note=tx.comment or tx.description,
        occurred_at=datetime.fromtimestamp(tx.time),
        external_id=tx.id,
        category=None
    )
