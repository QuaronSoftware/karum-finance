from sqlalchemy import (
    String,
    Integer,
    BigInteger
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class WalletORM(Base):
    __tablename__ = "wlts"

    id:             Mapped[int]         = mapped_column(Integer, primary_key=True)
    name:           Mapped[str]         = mapped_column(String)
    account_id:     Mapped[int]         = mapped_column(Integer)
    provider_id:    Mapped[str]         = mapped_column(String(64))
    external_id:    Mapped[str]         = mapped_column(String)
    currency:       Mapped[str]         = mapped_column(String(6), nullable=True)
    date_added:     Mapped[int]         = mapped_column(BigInteger)

