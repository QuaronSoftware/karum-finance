from sqlalchemy import (
    String,
    Integer,
    BigInteger
)
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.enum import BaseCurrencyCode
from app.domain.entity import AccountType

from .base import Base


class AccountORM(Base):
    __tablename__ = "wallets"

    id:             Mapped[int]                 = mapped_column(Integer, primary_key=True)
    name:           Mapped[str]                 = mapped_column(String)
    type:           Mapped[AccountType]         = mapped_column(String)
    currency:       Mapped[BaseCurrencyCode]    = mapped_column(String, default=BaseCurrencyCode.USD)
    owner_id:       Mapped[int]                 = mapped_column(Integer)    # Forigen key
    date_added:     Mapped[int]                 = mapped_column(BigInteger)

