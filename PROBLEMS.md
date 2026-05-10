# Phase 0 Design Problems

The starting cart works for a very small example, but it was intentionally written without design architecture. These are the main problems found before applying patterns.

## Problems Found by Me

1. **Product creation is inside `ShoppingCart`.** The cart should manage cart items, but it also decides how physical, digital, and subscription products are built. Adding a new product type requires editing the cart class.

2. **Discount rules are hard-coded in checkout.** Every new discount code adds another branch to the checkout method. This violates the Open/Closed Principle because existing checkout logic must change for each new discount.

3. **Payment selection is hard-coded in checkout.** The same method knows about credit card, PayPal, and bank transfer behavior. A real external payment provider would make this method even larger.

4. **Checkout has too many responsibilities.** It calculates totals, validates discounts, selects payment behavior, creates payment references, clears the cart, and returns the result. This makes the method difficult to test and risky to modify.

5. **The code depends on strings for important choices.** Product types, discount codes, and payment methods are plain strings. A typo becomes a runtime error and there is no clear extension point.

6. **Cart actions cannot be tracked or undone.** Adding and removing items directly mutates the cart. There is no object representing an action, so future undo, logging, or queueing behavior would be difficult.

## AI Review Comparison

**Prompt used:**

> This code has a cart class with product creation, discount conditionals, payment conditionals, and checkout logic in one place. Which design problems do you see? Which design patterns could solve them? Give a short explanation for each problem.

**AI summary:**

The AI identified the same core issues: a cart class doing too much, object creation mixed with business logic, discount branches that should become strategies, payment provider integration that could use an adapter, and checkout orchestration that could be hidden behind a facade. It also suggested representing cart operations as commands if undo or audit behavior is required.

**Comparison:**

My list focused first on the pain visible in the starting code. The AI helped connect each pain point to a pattern candidate. I accepted the Factory, Adapter, Facade, Strategy, and Command suggestions because they match the actual change pressures in this cart. I rejected adding Singleton because there is no shared global object in this small system.
