from dataclasses import dataclass
from typing import Protocol

from .cart import CartItem, ShoppingCart
from .products import Product


class CartCommand(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...


@dataclass
class AddItemCommand:
    cart: ShoppingCart
    product: Product
    quantity: int = 1
    previous_item: CartItem | None = None

    def execute(self) -> None:
        self.previous_item = self.cart.items.get(self.product.sku)
        self.cart.add_item(self.product, self.quantity)

    def undo(self) -> None:
        if self.previous_item is None:
            self.cart.remove_item(self.product.sku, self.quantity)
            return
        self.cart.items[self.product.sku] = self.previous_item


@dataclass
class RemoveItemCommand:
    cart: ShoppingCart
    sku: str
    quantity: int | None = None
    removed_item: CartItem | None = None
    removed_quantity: int = 0

    def execute(self) -> None:
        current = self.cart.items[self.sku]
        self.removed_item = current
        self.removed_quantity = (
            current.quantity
            if self.quantity is None or self.quantity >= current.quantity
            else self.quantity
        )
        self.cart.remove_item(self.sku, self.quantity)

    def undo(self) -> None:
        if self.removed_item is None or self.removed_quantity == 0:
            return
        self.cart.add_item(self.removed_item.product, self.removed_quantity)


class CartCommandHistory:
    def __init__(self) -> None:
        self._history: list[CartCommand] = []

    def execute(self, command: CartCommand) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if not self._history:
            raise IndexError("No command to undo")

        command = self._history.pop()
        command.undo()
