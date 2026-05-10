from decimal import Decimal

import pytest

from evolving_cart_patterns import PaymentAdapter


def test_payment_adapter_translates_external_provider_response() -> None:
    adapter = PaymentAdapter()

    receipt = adapter.pay(
        amount=Decimal("90.00"),
        payment_method="paypal",
        customer_email="student@example.com",
    )

    assert receipt.status == "approved"
    assert receipt.reference.startswith("provider-paypal-student@example.com")


def test_payment_adapter_rejects_unknown_payment_method() -> None:
    adapter = PaymentAdapter()

    with pytest.raises(ValueError, match="Unknown payment method"):
        adapter.pay("10.00", "cash", "student@example.com")
