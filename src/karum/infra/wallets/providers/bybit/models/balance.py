from pydantic import BaseModel
from typing import List, Dict, Any


class Balance(BaseModel):
    coin: str
    transferBalance: str
    walletBalance: str
    bonus: str


class Result(BaseModel):
    memberId: str
    accountType: str
    balance: List[Balance]


class Response(BaseModel):
    retCode: int
    retMsg: str
    result: Result
    retExtInfo: Dict[str, Any]
    time: int