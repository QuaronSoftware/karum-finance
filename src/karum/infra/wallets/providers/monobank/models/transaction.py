from typing import List, Optional
from pydantic import BaseModel


class MonobankTransaction(BaseModel):
    id: str
    time: int
    description: str
    mcc: int
    originalMcc: int
    hold: bool
    amount: int
    operationAmount: int
    currencyCode: int
    commissionRate: int
    cashbackAmount: int
    balance: int

    comment: Optional[str] = None
    receiptId: Optional[str] = None
    invoiceId: Optional[str] = None
    counterEdrpou: Optional[str] = None
    counterIban: Optional[str] = None
    counterName: Optional[str] = None

MonobankListTransaction = List[MonobankTransaction]
