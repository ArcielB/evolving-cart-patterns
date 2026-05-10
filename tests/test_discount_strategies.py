from decimal import Decimal

from evolving_cart_patterns import (
    CheckoutFacade,
    FixedAmountDiscount,
    LoyaltyPointsDiscount,
    PercentageDiscount,
    ShoppingCart,
    ThresholdPercentageDiscount,
)


def test_multiple_discount_strategies() -> None:
    subtotal = Decimal("100.00")

    assert PercentageDiscount("WELCOME10", Decimal("0.10")).calculate(
        subtotal
    ) == Decimal("10.00")
    assert ThresholdPercentageDiscount(
        "BULK15", Decimal("0.15"), Decimal("100.00")
    ).calculate(subtotal) == Decimal("15.00")
    assert FixedAmountDiscount("COUPON5", Decimal("5.00")).calculate(
        subtotal
    ) == Decimal("5.00")


def test_ocp_new_discount_strategy_works_without_checkout_changes() -> None:
    class StudentDiscount:
        name = "Student flat discount"

        def calculate(self, subtotal: Decimal) -> Decimal:
            return Decimal("12.50")

    cart = ShoppingCart()
    cart.add_product("COURSE-1", "Monthly Course", "100.00", "subscription")
    facade = CheckoutFacade(cart)

    result = facade.checkout(
        payment_method="paypal",
        customer_email="student@example.com",
        discount_strategy=StudentDiscount(),
    )

    assert result.discount == Decimal("12.50")
    assert result.total == Decimal("87.50")


def test_loyalty_points_discount_is_extension_example() -> None:
    discount = LoyaltyPointsDiscount("LOYALTY", points=250)

    assert discount.calculate(Decimal("100.00")) == Decimal("2.50")
