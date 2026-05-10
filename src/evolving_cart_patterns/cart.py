from dataclasses import dataclass
from decimal import Decimal

from .factories import ProductFactory
from .money import money
from .products import Product


@dataclass(frozen=True)
class CartItem:
    product: Product
    quantity: int

    @property
    def line_total(self) -> Decimal:
        return money(self.product.price * self.quantity)


@dataclass(frozen=True)
class CheckoutResult:
    subtotal: Decimal
    discount: Decimal
    total: Decimal
    payment_status: str
    payment_reference: str
    item_count: int


class ShoppingCart:
    def __init__(self, product_factory: ProductFactory | None = None) -> None:
        self.items: dict[str, CartItem] = {}
        self.product_factory = product_factory or ProductFactory()

    def create_product(
        self, sku: str, name: str, price: Decimal | int | str, product_type: str
    ) -> Product:
        return self.product_factory.create_product(sku, name, price, product_type)

    def add_product(
        self,
        sku: str,
        name: str,
        price: Decimal | int | str,
        product_type: str,
        quantity: int = 1,
    ) -> None:
        product = self.create_product(sku, name, price, product_type)
        self.add_item(product, quantity)

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        current = self.items.get(product.sku)
        if current is None:
            self.items[product.sku] = CartItem(product=product, quantity=quantity)
        else:
            self.items[product.sku] = CartItem(
                product=product, quantity=current.quantity + quantity
            )

    def remove_item(self, sku: str, quantity: int | None = None) -> None:
        if sku not in self.items:
            raise KeyError(f"Product {sku} is not in the cart")

        current = self.items[sku]
        if quantity is None or quantity >= current.quantity:
            del self.items[sku]
            return

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.items[sku] = CartItem(
            product=current.product, quantity=current.quantity - quantity
        )

    def subtotal(self) -> Decimal:
        total = Decimal("0.00")
        for item in self.items.values():
            total += item.line_total
        return money(total)

    def item_count(self) -> int:
        return sum(item.quantity for item in self.items.values())

    def clear(self) -> None:
        self.items.clear()

    def checkout(
        self,
        discount_code: str | None,
        payment_method: str,
        customer_email: str,
    ) -> CheckoutResult:
        from .checkout import CheckoutFacade

        return CheckoutFacade(self).checkout(
            discount_code=discount_code,
            payment_method=payment_method,
            customer_email=customer_email,
        )
