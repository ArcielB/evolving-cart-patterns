from decimal import Decimal

from .cart import CheckoutResult, ShoppingCart
from .money import money
from .payments import PaymentAdapter


class CheckoutFacade:
    def __init__(
        self, cart: ShoppingCart, payment_adapter: PaymentAdapter | None = None
    ) -> None:
        self.cart = cart
        self.payment_adapter = payment_adapter or PaymentAdapter()

    def checkout(
        self,
        discount_code: str | None,
        payment_method: str,
        customer_email: str,
    ) -> CheckoutResult:
        subtotal = self.cart.subtotal()
        item_count = self.cart.item_count()
        discount = self._calculate_discount(discount_code, subtotal)
        total = money(subtotal - discount)
        receipt = self.payment_adapter.pay(total, payment_method, customer_email)

        self.cart.clear()
        return CheckoutResult(
            subtotal=subtotal,
            discount=discount,
            total=total,
            payment_status=receipt.status,
            payment_reference=receipt.reference,
            item_count=item_count,
        )

    def _calculate_discount(
        self, discount_code: str | None, subtotal: Decimal
    ) -> Decimal:
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

        return money(discount)
