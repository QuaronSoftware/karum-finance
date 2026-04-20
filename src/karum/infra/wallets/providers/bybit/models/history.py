from decimal import Decimal

from pydantic import BaseModel
from typing import List, Optional, Dict


class TransactionItem(BaseModel):
    memberId: str
    currency: str
    ioDirection: str
    txnAmt: Decimal
    afterAmt: Decimal
    createTime: int
    showBusiType: str
    showBusiTypeEn: str
    description: str
    descriptionEn: str


class ResultModel(BaseModel):
    nextPageCursor: Optional[str]
    list: List[TransactionItem]


class BybitFundingHistoryResponse(BaseModel):
    retCode: int
    retMsg: str
    result: ResultModel
    retExtInfo: Dict
    time: int