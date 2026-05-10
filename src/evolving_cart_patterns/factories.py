from abc import ABC, abstractmethod
from decimal import Decimal

from .money import money
from .products import Product


class ProductCreator(ABC):
    @abstractmethod
    def create_product(
        self, sku: str, name: str, price: Decimal | int | str
    ) -> Product:
        ...

    def _build_product(
        self,
        sku: str,
        name: str,
        price: Decimal | int | str,
        product_type: str,
        shipping_required: bool,
        tax_rate: Decimal,
    ) -> Product:
        return Product(
            sku=sku,
            name=name,
            price=money(price),
            product_type=product_type,
            shipping_required=shipping_required,
            tax_rate=tax_rate,
        )


class PhysicalProductCreator(ProductCreator):
    def create_product(
        self, sku: str, name: str, price: Decimal | int | str
    ) -> Product:
        return self._build_product(sku, name, price, "physical", True, Decimal("0.18"))


class DigitalProductCreator(ProductCreator):
    def create_product(
        self, sku: str, name: str, price: Decimal | int | str
    ) -> Product:
        return self._build_product(sku, name, price, "digital", False, Decimal("0.08"))


class SubscriptionProductCreator(ProductCreator):
    def create_product(
        self, sku: str, name: str, price: Decimal | int | str
    ) -> Product:
        return self._build_product(
            sku, name, price, "subscription", False, Decimal("0.00")
        )


class ProductFactory:
    def __init__(self, creators: dict[str, ProductCreator] | None = None) -> None:
        self._creators = creators or {
            "physical": PhysicalProductCreator(),
            "digital": DigitalProductCreator(),
            "subscription": SubscriptionProductCreator(),
        }

    def create_product(
        self, sku: str, name: str, price: Decimal | int | str, product_type: str
    ) -> Product:
        try:
            creator = self._creators[product_type]
        except KeyError as exc:
            raise ValueError(f"Unknown product type: {product_type}") from exc

        return creator.create_product(sku, name, price)
