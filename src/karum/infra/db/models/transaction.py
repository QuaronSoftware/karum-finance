from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DECIMAL,
    Index,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from karum.domain.entity import TransactionType
from .base import Base


class TransactionORM(Base):
    __tablename__ = "txs"
    __table_args__ = (
        Index("ix_txs_wallet_id", "wallet_id"),
        Index("ix_txs_from_wallet_id", "from_wallet_id"),
        Index("ix_txs_to_wallet_id", "to_wallet_id"),
        Index("ix_txs_occurred_at", "occurred_at"),
        Index("ix_txs_type", "type"),
        UniqueConstraint("external_id", name="uq_txs_external_id"),
    )

    id:             Mapped[int]             = mapped_column(Integer, primary_key=True)
    type:           Mapped[TransactionType] = mapped_column(String(12))

    # Type: [income | expense]
    asset:          Mapped[str]             = mapped_column(String(6), nullable=True)  # Up to 3;
    amount:         Mapped[Decimal]         = mapped_column(DECIMAL, nullable=True)    # Big float
    wallet_id:      Mapped[int]             = mapped_column(Integer, nullable=True)

    # From
    from_asset:     Mapped[str]             = mapped_column(String(6), nullable=True)  # Up to 3;
    from_amount:    Mapped[Decimal]         = mapped_column(DECIMAL, nullable=True)    # Big float
    from_wallet_id: Mapped[int]             = mapped_column(Integer, nullable=True)

    # To
    to_asset:       Mapped[str]             = mapped_column(String(6), nullable=True)  # Up to 3;
    to_amount:      Mapped[Decimal]         = mapped_column(DECIMAL, nullable=True)    # Big float
    to_wallet_id:   Mapped[int]             = mapped_column(Integer, nullable=True)

    note:           Mapped[str]             = mapped_column(String(512), nullable=True)
    external_id:    Mapped[str]             = mapped_column(String(64), nullable=True)
    category_id:    Mapped[str]             = mapped_column(String(28), nullable=True)
    occurred_at:    Mapped[BigInteger]      = mapped_column(BigInteger)
