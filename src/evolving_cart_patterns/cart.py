from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


def money(value: Decimal | int | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: Decimal
    product_type: str
    shipping_required: bool
    tax_rate: Decimal


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
    def __init__(self) -> None:
        self.items: dict[str, CartItem] = {}

    def create_product(
        self, sku: str, name: str, price: Decimal | int | str, product_type: str
    ) -> Product:
        if product_type == "physical":
            return Product(
                sku=sku,
                name=name,
                price=money(price),
                product_type="physical",
                shipping_required=True,
                tax_rate=Decimal("0.18"),
            )
        if product_type == "digital":
            return Product(
                sku=sku,
                name=name,
                price=money(price),
                product_type="digital",
                shipping_required=False,
                tax_rate=Decimal("0.08"),
            )
        if product_type == "subscription":
            return Product(
                sku=sku,
                name=name,
                price=money(price),
                product_type="subscription",
                shipping_required=False,
                tax_rate=Decimal("0.00"),
            )
        raise ValueError(f"Unknown product type: {product_type}")

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

    def checkout(
        self,
        discount_code: str | None,
        payment_method: str,
        customer_email: str,
    ) -> CheckoutResult:
        subtotal = self.subtotal()
        item_count = sum(item.quantity for item in self.items.values())

        if discount_code is None or discount_code == "":
            discount = Decimal("0.00")
        elif discount_code == "WELCOME10":
            discount = subtotal * Decimal("0.10")
        elif discount_code == "VIP20":
            discount = subtotal * Decimal("0.20")
        elif discount_code == "BULK15":
            if subtotal >= Decimal("100.00"):
                discount = subtotal * Decimal("0.15")
            else:
                discount = Decimal("0.00")
        else:
            raise ValueError(f"Unknown discount code: {discount_code}")

        discount = money(discount)
        total = money(subtotal - discount)

        if payment_method == "credit_card":
            payment_status = "approved"
            payment_reference = f"cc-{customer_email}-{total}"
        elif payment_method == "paypal":
            payment_status = "approved"
            payment_reference = f"paypal-{customer_email}-{total}"
        elif payment_method == "bank_transfer":
            payment_status = "pending"
            payment_reference = f"bank-{customer_email}-{total}"
        else:
            raise ValueError(f"Unknown payment method: {payment_method}")

        self.items.clear()
        return CheckoutResult(
            subtotal=subtotal,
            discount=discount,
            total=total,
            payment_status=payment_status,
            payment_reference=payment_reference,
            item_count=item_count,
        )
