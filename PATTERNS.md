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
