from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, List


class OKXAccountBill(BaseModel):
    # ids
    bill_id: str = Field(alias="billId")
    order_id: Optional[str] = Field(default=None, alias="ordId")
    trade_id: Optional[str] = Field(default=None, alias="tradeId")
    client_order_id: Optional[str] = Field(default=None, alias="clOrdId")

    # asset
    currency: str = Field(alias="ccy")

    # balances
    balance: Decimal = Field(alias="bal")
    balance_change: Decimal = Field(alias="balChg")

    # trade info
    instrument_id: Optional[str] = Field(default=None, alias="instId")
    instrument_type: Optional[str] = Field(default=None, alias="instType")

    price: Optional[Decimal] = Field(default=None, alias="px")
    size: Optional[Decimal] = Field(default=None, alias="sz")

    fee: Optional[Decimal] = None
    pnl: Optional[Decimal] = None

    # fill data
    fill_price_index: Optional[Decimal] = Field(default=None, alias="fillIdxPx")
    fill_price_usd: Optional[Decimal] = Field(default=None, alias="fillPxUsd")

    fill_time: Optional[int] = Field(default=None, alias="fillTime")

    # positions
    position_balance: Optional[Decimal] = Field(default=None, alias="posBal")
    position_balance_change: Optional[Decimal] = Field(default=None, alias="posBalChg")

    # earn
    earn_amount: Optional[Decimal] = Field(default=None, alias="earnAmt")
    earn_apr: Optional[Decimal] = Field(default=None, alias="earnApr")

    # misc
    exec_type: Optional[str] = Field(default=None, alias="execType")
    margin_mode: Optional[str] = Field(default=None, alias="mgnMode")

    from_address: Optional[str] = Field(default=None, alias="from")
    to_address: Optional[str] = Field(default=None, alias="to")

    sub_type: Optional[str] = Field(default=None, alias="subType")
    type: str

    notes: Optional[str] = None
    tag: Optional[str] = None

    # timestamp
    timestamp: int = Field(alias="ts")

    @field_validator(
        "price",
        "size",
        "fee",
        "pnl",
        "fill_price_index",
        "fill_price_usd",
        "position_balance",
        "position_balance_change",
        "earn_amount",
        "earn_apr",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, value):
        if value in ("", None):
            return None
        return Decimal(value)


class OKXAccountBillResponse(BaseModel):
    code: str
    msg: str
    data: List[OKXAccountBill]