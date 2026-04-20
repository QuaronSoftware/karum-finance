from datetime import datetime
from app.domain.entity import Transaction
from .models import OKXAccountBill, OKXBill


def to_transaction(wallet_id: str, tx: OKXAccountBill | OKXBill) -> Transaction:
    if tx.balance_change>=0:
        return Transaction.new_income(
            id=None,
            amount=abs(tx.balance_change),
            symbol=tx.currency,
            wallet_id=wallet_id,
            note=tx.notes,
            occurred_at=datetime.fromtimestamp(tx.timestamp/1000),
            external_id=tx.bill_id,
            category=None
        )
    return Transaction.new_expense(
        id=None,
        amount=abs(tx.balance_change),
        symbol=tx.currency,
        wallet_id=wallet_id,
        note=tx.notes,
        occurred_at=datetime.fromtimestamp(tx.timestamp/1000),
        external_id=tx.bill_id,
        category=None
    )


