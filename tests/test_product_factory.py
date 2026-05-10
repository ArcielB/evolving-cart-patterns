from decimal import Decimal

import pytest

from evolving_cart_patterns import DigitalProductCreator, ProductFactory


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


def test_concrete_creator_owns_product_creation_rule() -> None:
    creator = DigitalProductCreator()

    product = creator.create_product("PDF-2", "Factory Method Notes", "12.00")

    assert product.product_type == "digital"
    assert product.shipping_required is False
    assert product.tax_rate == Decimal("0.08")
