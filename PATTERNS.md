# Pattern Decisions

This file records the design patterns applied as the project evolves.

## Phase 0

No design pattern has been applied yet. The baseline intentionally keeps product creation, discount selection, payment selection, and checkout orchestration inside one cart class so the later refactorings solve visible problems instead of imaginary ones.

## Phase 1 - Factory Method

**Where:** `src/evolving_cart_patterns/factories.py`

**Problem solved:** In Phase 0, `ShoppingCart` had to know how every product type was created. This mixed object creation with cart management and forced the cart class to change whenever a product construction rule changed.

**Implementation:** `ProductCreator` declares the `create_product(...)` factory method. `PhysicalProductCreator`, `DigitalProductCreator`, and `SubscriptionProductCreator` implement that method for their own product type. `ProductFactory` is a small registry that selects the correct creator from the requested product type, and `ShoppingCart.add_product(...)` delegates to it instead of building products itself.

**Benefit:** Product creation is centralized and testable, but the actual construction rules are no longer one conditional block. The cart now focuses more on cart operations, while new product creators can be added without changing cart behavior.

**Rejected alternatives:** Abstract Factory was too large for this project because there are no families of related product objects. Singleton was unnecessary because product creation does not need global shared state.
