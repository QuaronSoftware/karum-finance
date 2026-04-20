from datetime import datetime
from karum.domain.entity import Transaction
from .models import TransactionItem


def to_transaction(wallet_id: str, tx: TransactionItem) -> Transaction:
    if tx.ioDirection == 'I':
        return Transaction.new_income(
            id=None,
            amount=tx.txnAmt,
            symbol=tx.currency,
            wallet_id=wallet_id,
            note=tx.descriptionEn,
            occurred_at=datetime.fromtimestamp(tx.createTime),
            external_id=None,
            category=None
        )
    return Transaction.new_expense(
        id=None,
        amount=tx.txnAmt,
        symbol=tx.currency,
        wallet_id=wallet_id,
        note=tx.descriptionEn,
        occurred_at=datetime.fromtimestamp(tx.createTime),
        external_id=None,
        category=None
    )
