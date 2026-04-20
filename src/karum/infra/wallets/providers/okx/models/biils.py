from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Optional


class OKXBill(BaseModel):
    bill_id: str = Field(alias="billId")
    client_id: Optional[str] = Field(default=None, alias="clientId")
    currency: str = Field(alias="ccy")
    balance_change: Decimal = Field(alias="balChg")
    balance: Decimal = Field(alias="bal")
    type: str
    timestamp: int = Field(alias="ts")
    notes: Optional[str] = None


class OKXBillResponse(BaseModel):
    code: str
    msg: str
    data: List[OKXBill]