from decimal import Decimal

from .money import money
from .products import Product


class ProductFactory:
    _PRODUCT_RULES = {
        "physical": {"shipping_required": True, "tax_rate": Decimal("0.18")},
        "digital": {"shipping_required": False, "tax_rate": Decimal("0.08")},
        "subscription": {"shipping_required": False, "tax_rate": Decimal("0.00")},
    }

    def create_product(
        self, sku: str, name: str, price: Decimal | int | str, product_type: str
    ) -> Product:
        try:
            rule = self._PRODUCT_RULES[product_type]
        except KeyError as exc:
            raise ValueError(f"Unknown product type: {product_type}") from exc

        return Product(
            sku=sku,
            name=name,
            price=money(price),
            product_type=product_type,
            shipping_required=rule["shipping_required"],
            tax_rate=rule["tax_rate"],
        )
