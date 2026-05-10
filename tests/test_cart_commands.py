from evolving_cart_patterns import (
    AddItemCommand,
    CartCommandHistory,
    ProductFactory,
    RemoveItemCommand,
    ShoppingCart,
)


def test_add_item_command_can_be_undone() -> None:
    cart = ShoppingCart()
    product = ProductFactory().create_product("PDF-1", "Python Guide", "25.50", "digital")
    history = CartCommandHistory()

    history.execute(AddItemCommand(cart, product, quantity=2))
    history.undo_last()

    assert "PDF-1" not in cart.items


def test_add_item_command_undo_restores_existing_item() -> None:
    cart = ShoppingCart()
    factory = ProductFactory()
    original = factory.create_product("PDF-1", "Python Guide", "25.50", "digital")
    replacement = factory.create_product("PDF-1", "Updated Guide", "30.00", "digital")
    cart.add_item(original, quantity=1)
    history = CartCommandHistory()

    history.execute(AddItemCommand(cart, replacement, quantity=2))
    history.undo_last()

    assert cart.items["PDF-1"].quantity == 1
    assert cart.items["PDF-1"].product == original


def test_remove_item_command_can_be_undone() -> None:
    cart = ShoppingCart()
    product = ProductFactory().create_product("BOOK-1", "Design Patterns", "50.00", "physical")
    cart.add_item(product, quantity=3)
    history = CartCommandHistory()

    history.execute(RemoveItemCommand(cart, "BOOK-1", quantity=2))
    history.undo_last()

    assert cart.items["BOOK-1"].quantity == 3
