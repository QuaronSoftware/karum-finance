from typing import List, Optional
from pydantic import BaseModel


class MonobankAccount(BaseModel):
    id: str
    sendId: str
    balance: int
    creditLimit: int
    type: str
    currencyCode: int
    cashbackType: Optional[str] = None
    maskedPan: Optional[List[str]] = None
    iban: str


class Jar(BaseModel):
    id: str
    sendId: str
    title: str
    description: str
    currencyCode: int
    balance: int
    goal: int


class ManagedClientAccount(BaseModel):
    id: str
    balance: int
    creditLimit: int
    type: str
    currencyCode: int
    iban: str


class ManagedClient(BaseModel):
    clientId: str
    tin: int
    name: str
    accounts: List[ManagedClientAccount]


class MonobankPersonalInfo(BaseModel):
    clientId: str
    name: str
    webHookUrl: str
    permissions: str
    accounts: List[MonobankAccount]
    jars: List[Jar] = []
    managedClients: List[ManagedClient] = []
