from decimal import Decimal

import pytest

from evolving_cart_patterns import ProductFactory


def test_factory_creates_digital_product() -> None:
    factory = ProductFactory()

    product = factory.create_product("PDF-1", "Python Guide", "25.50", "digital")

    assert product.price == Decimal("25.50")
    assert product.product_type == "digital"
    assert product.shipping_required is False
    assert product.tax_rate == Decimal("0.08")


def test_factory_rejects_unknown_product_type() -> None:
    factory = ProductFactory()

    with pytest.raises(ValueError, match="Unknown product type"):
        factory.create_product("BAD-1", "Broken", "1.00", "unknown")
