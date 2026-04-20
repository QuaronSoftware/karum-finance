from enum import Enum


class BaseCurrencyCode(str, Enum):
    UAH = "UAH"
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"
