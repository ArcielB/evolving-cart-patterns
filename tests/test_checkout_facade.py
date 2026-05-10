from decimal import Decimal

from evolving_cart_patterns import CheckoutFacade, ShoppingCart


def test_checkout_facade_completes_checkout() -> None:
    cart = ShoppingCart()
    cart.add_product("COURSE-1", "Monthly Course", "100.00", "subscription")
    facade = CheckoutFacade(cart)

    result = facade.checkout(
        discount_code="VIP20",
        payment_method="credit_card",
        customer_email="student@example.com",
    )

    assert result.subtotal == Decimal("100.00")
    assert result.discount == Decimal("20.00")
    assert result.total == Decimal("80.00")
    assert result.payment_status == "approved"
    assert result.payment_reference.startswith("provider-credit_card")
    assert result.item_count == 1
    assert cart.items == {}
