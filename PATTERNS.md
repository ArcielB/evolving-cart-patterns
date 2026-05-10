# Pattern Decisions

This file records the design patterns applied as the project evolves.

## Phase 0

No design pattern has been applied yet. The baseline intentionally keeps product creation, discount selection, payment selection, and checkout orchestration inside one cart class so the later refactorings solve visible problems instead of imaginary ones.

## Phase 1 - Simple Factory / Factory Method Family

**Where:** `src/evolving_cart_patterns/factories.py`

**Problem solved:** In Phase 0, `ShoppingCart` had to know how every product type was created. This mixed object creation with cart management and forced the cart class to change whenever a product construction rule changed.

**Implementation:** `ProductFactory.create_product(...)` receives the product type and creates a configured `Product` object. `ShoppingCart.add_product(...)` delegates to the factory instead of building products itself.

**Benefit:** Product creation is centralized and testable. The cart now focuses more on cart operations, while product construction rules live in one dedicated class.

**Rejected alternatives:** Abstract Factory was too large for this project because there are no families of related product objects. Singleton was unnecessary because the factory does not manage shared state.

## Phase 2 - Facade

**Where:** `src/evolving_cart_patterns/checkout.py`

**Problem solved:** Checkout required several steps: subtotal calculation, discount calculation, payment processing, cart clearing, and result creation. Client code should not need to coordinate all of those details.

**Implementation:** `CheckoutFacade.checkout(...)` is the clean entry point for checkout. It uses the cart and payment adapter internally and returns a `CheckoutResult`.

**Benefit:** Checkout usage is simpler, and orchestration logic is separated from cart item management.

**Rejected alternatives:** A large service class without a clear pattern name would still work, but Facade better describes the intention: hide a group of subsystem operations behind a small interface.

## Phase 2 - Adapter

**Where:** `src/evolving_cart_patterns/payments.py`

**Problem solved:** The simulated external provider uses `submit_payment(payload)` and returns provider-style keys. The application should not depend on those provider details.

**Implementation:** `PaymentAdapter.pay(...)` converts application arguments into the provider payload and converts the provider response into a `PaymentReceipt`.

**Benefit:** The rest of the application can use a stable payment interface even if the external provider changes its payload format.

**Rejected alternatives:** Proxy was not needed because there is no remote access control or caching concern. Decorator was not needed because payment behavior is not being layered with optional responsibilities.
