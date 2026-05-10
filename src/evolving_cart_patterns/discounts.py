from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from .money import money


class DiscountStrategy(Protocol):
    name: str

    def calculate(self, subtotal: Decimal) -> Decimal:
        ...


@dataclass(frozen=True)
class NoDiscount:
    name: str = "No discount"

    def calculate(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")


@dataclass(frozen=True)
class PercentageDiscount:
    name: str
    rate: Decimal

    def calculate(self, subtotal: Decimal) -> Decimal:
        return money(subtotal * self.rate)


@dataclass(frozen=True)
class ThresholdPercentageDiscount:
    name: str
    rate: Decimal
    minimum_subtotal: Decimal

    def calculate(self, subtotal: Decimal) -> Decimal:
        if subtotal < self.minimum_subtotal:
            return Decimal("0.00")
        return money(subtotal * self.rate)


@dataclass(frozen=True)
class FixedAmountDiscount:
    name: str
    amount: Decimal

    def calculate(self, subtotal: Decimal) -> Decimal:
        if subtotal <= Decimal("0.00"):
            return Decimal("0.00")
        return money(min(self.amount, subtotal))


@dataclass(frozen=True)
class LoyaltyPointsDiscount:
    name: str
    points: int
    cents_per_point: Decimal = Decimal("0.01")

    def calculate(self, subtotal: Decimal) -> Decimal:
        value = Decimal(self.points) * self.cents_per_point
        return money(min(value, subtotal))
