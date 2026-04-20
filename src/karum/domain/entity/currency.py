from dataclasses import dataclass
from ..enum import BaseCurrencyCode


@dataclass(frozen=True)
class Currency:
    code: BaseCurrencyCode
    numeric: int
    precision: int


BASE_CURRENCIES = {
    BaseCurrencyCode.UAH: Currency(BaseCurrencyCode.UAH, 980, 2),
    BaseCurrencyCode.USD: Currency(BaseCurrencyCode.USD, 840, 2),
    BaseCurrencyCode.EUR: Currency(BaseCurrencyCode.EUR, 978, 2),
    BaseCurrencyCode.PLN: Currency(BaseCurrencyCode.PLN, 985, 2)
}