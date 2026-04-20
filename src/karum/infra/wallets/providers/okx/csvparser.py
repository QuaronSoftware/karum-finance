import csv
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from karum.domain.entity import Transaction


class OKXCSVRow:
    def __init__(
        self,
        bill_id: str,
        order_id: Optional[str],
        timestamp: datetime,
        trade_type: str,
        symbol: str,
        action: str,
        amount: Decimal,
        price: Optional[Decimal],
        fee: Optional[Decimal],
        pnl: Optional[Decimal],
        balance: Optional[Decimal],
        balance_change: Optional[Decimal],
    ):
        self.bill_id = bill_id
        self.order_id = order_id
        self.timestamp = timestamp
        self.trade_type = trade_type
        self.symbol = symbol
        self.action = action
        self.amount = amount
        self.price = price
        self.fee = fee
        self.pnl = pnl
        self.balance = balance
        self.balance_change = balance_change
    
    def to_transaction(self, wallet_id: str):
        if self.balance_change>0:
            return Transaction.new_income(
                id=None,
                amount=abs(self.balance_change),
                symbol=self.symbol,
                wallet_id=wallet_id,
                note=self.action,
                occurred_at=self.timestamp,
                external_id=self.bill_id,
                category=None
            )
        return Transaction.new_expense(
            id=None,
            amount=abs(self.balance_change),
            symbol=self.symbol,
            wallet_id=wallet_id,
            note=self.action,
            occurred_at=self.timestamp,
            external_id=self.bill_id,
            category=None
        )

def _parse_decimal(value: str) -> Optional[Decimal]:
    if not value:
        return None
    return Decimal(value)


def _parse_time(value: str) -> datetime:
    # OKX формат: "2023-09-18 12:34:56"
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")



def parse_okx_csv(path: str) -> list[OKXCSVRow]:
    rows = []

    with open(path, "r", encoding="utf-8-sig") as f:
        # 1️⃣ пропускаємо мета рядок
        next(f)

        # 2️⃣ читаємо header
        header = next(f).strip().split(",")

        # чистимо BOM і пробіли
        header = [h.replace('\ufeff', '').strip() for h in header]

        # 3️⃣ створюємо DictReader вже з нормальним header
        dict_reader = csv.DictReader(f, fieldnames=header)

        for row in dict_reader:
            # чистимо значення
            row = {
                k: (v.strip().replace('\ufeff', '') if v else v)
                for k, v in row.items()
            }

            rows.append(
                OKXCSVRow(
                    bill_id=row["id"],
                    order_id=row["Order id"] or None,
                    timestamp=_parse_time(row["Time"]),
                    trade_type=row["Trade Type"],
                    symbol=row["Balance Unit"],
                    action=row["Action"],
                    amount=_parse_decimal(row["Amount"]) or Decimal(0),
                    price=_parse_decimal(row["Filled Price"]),
                    fee=_parse_decimal(row["Fee"]),
                    pnl=_parse_decimal(row["PnL"]),
                    balance=_parse_decimal(row["Balance"]),
                    balance_change=_parse_decimal(row["Balance Change"]),
                )
            )

    return rows