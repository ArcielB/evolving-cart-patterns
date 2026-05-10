from decimal import Decimal

import pytest

from evolving_cart_patterns import PercentageDiscount, ShoppingCart


def test_add_products_and_calculate_subtotal() -> None:
    cart = ShoppingCart()

    cart.add_product("BOOK-1", "Design Patterns Book", "50.00", "physical", quantity=2)
    cart.add_product("PDF-1", "Python Guide", "25.50", "digital")

    assert cart.subtotal() == Decimal("125.50")
    assert cart.items["BOOK-1"].quantity == 2


def test_remove_product_quantity() -> None:
    cart = ShoppingCart()
    cart.add_product("BOOK-1", "Design Patterns Book", "50.00", "physical", quantity=3)

    cart.remove_item("BOOK-1", quantity=1)

    assert cart.items["BOOK-1"].quantity == 2


def test_checkout_applies_discount_and_selects_payment() -> None:
    cart = ShoppingCart()
    cart.add_product("COURSE-1", "Monthly Course", "100.00", "subscription")

    result = cart.checkout(
        payment_method="credit_card",
        customer_email="student@example.com",
        discount_strategy=PercentageDiscount("WELCOME10", Decimal("0.10")),
    )

    assert result.subtotal == Decimal("100.00")
    assert result.discount == Decimal("10.00")
    assert result.total == Decimal("90.00")
    assert result.payment_status == "approved"
    assert result.payment_reference.startswith("provider-credit_card-student@example.com")
    assert cart.items == {}


def test_unknown_payment_is_rejected() -> None:
    cart = ShoppingCart()
    cart.add_product("PDF-1", "Python Guide", "25.50", "digital")

    with pytest.raises(ValueError, match="Unknown payment method"):
        cart.checkout("cash", "student@example.com")
