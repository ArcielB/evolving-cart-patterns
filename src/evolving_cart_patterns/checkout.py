from .cart import CheckoutResult, ShoppingCart
from .discounts import DiscountStrategy, NoDiscount
from .money import money
from .payments import PaymentAdapter


class CheckoutFacade:
    def __init__(
        self,
        cart: ShoppingCart,
        payment_adapter: PaymentAdapter | None = None,
        discount_strategy: DiscountStrategy | None = None,
    ) -> None:
        self.cart = cart
        self.payment_adapter = payment_adapter or PaymentAdapter()
        self.discount_strategy = discount_strategy or NoDiscount()

    def checkout(
        self,
        payment_method: str,
        customer_email: str,
        discount_strategy: DiscountStrategy | None = None,
    ) -> CheckoutResult:
        subtotal = self.cart.subtotal()
        item_count = self.cart.item_count()
        strategy = discount_strategy or self.discount_strategy
        discount = money(strategy.calculate(subtotal))
        if discount > subtotal:
            discount = subtotal

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
