# Phase 3 AI Log - Behavioral Patterns

## Pair Programming Session

Session length: approximately 30 minutes of AI-assisted design and implementation.

## Prompts

I asked:

> Checkout still contains discount conditionals. How can Strategy make discounts open for extension without changing checkout every time?

I also asked:

> Cart add/remove actions may need undo or audit behavior later. Would Command be a good fit, and what should each command own?

## AI Response Summary

The AI recommended:

- Create a `DiscountStrategy` interface with concrete strategies such as percentage, threshold, fixed amount, and loyalty points.
- Make `CheckoutFacade` receive a strategy object instead of reading discount-code strings.
- Create cart command objects with `execute()` and `undo()` methods.
- Keep command history separate from the cart so the cart remains a simple domain object.

## What I Implemented

- `DiscountStrategy` protocol.
- `NoDiscount`, `PercentageDiscount`, `ThresholdPercentageDiscount`, `FixedAmountDiscount`, and `LoyaltyPointsDiscount`.
- `CheckoutFacade.checkout(...)` now accepts a strategy object.
- `AddItemCommand`, `RemoveItemCommand`, and `CartCommandHistory`.
- An OCP test that defines a new `StudentDiscount` inside the test and passes it to checkout without changing cart or checkout code.

## Critical Review

The AI first suggested keeping a dictionary of discount codes inside checkout. I rejected that because adding a new discount code would still require editing checkout or a central resolver. Passing a strategy object is a clearer OCP demonstration for this homework.

The AI also suggested making commands responsible for creating products. I rejected that because product creation already belongs to `ProductFactory`; commands should represent actions against the cart.

During final review, I found one missed Command detail: undoing an add operation should restore the previous cart item exactly when the SKU already existed, not only subtract the added quantity. I updated `AddItemCommand` to snapshot the previous `CartItem` before execution and added a regression test for that case.

## AI Without This Phase

Without AI, this phase would likely take about 60-90 minutes because I would spend more time comparing Strategy and Command boundaries. AI was most useful for quickly listing the design options. It was least useful when it suggested a discount-code dictionary, because that would weaken the Open/Closed Principle demonstration.

## Result

Discount behavior is now interchangeable, and new discount classes can be added without modifying checkout logic. Cart actions can also be executed and undone through command objects, including exact restoration of a previous cart item after an add command is undone.
