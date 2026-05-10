# Phase 2 AI Log - Structural Patterns

## Prompt

I asked:

> Adapter pattern burada uygun mu, yoksa Facade mı? Bu e-commerce cart için farkını açıkla. Payment provider entegrasyonu ve checkout kullanımı ayrı problemler mi?

## AI Response Summary

The AI explained that Adapter and Facade solve different structural problems:

- Adapter is useful when the application wants one interface but an external provider exposes another interface.
- Facade is useful when client code should not know the steps needed to complete checkout.

It suggested using both if payment integration and checkout orchestration are separate sources of complexity.

## Decision

I used both patterns:

- `PaymentAdapter` adapts `ExternalPaymentProvider.submit_payment(...)` to the simpler application method `pay(...)`.
- `CheckoutFacade` gives client code one checkout entry point and hides subtotal, discount, payment, cart clearing, and result creation steps.

## Critical Review

The AI initially treated the payment adapter as if it should also calculate discounts. I rejected that because it would mix business rules with an integration boundary. Discount selection remains visible for Phase 3, where it will be replaced by Strategy.

## Alternatives Rejected

- Decorator was rejected because this phase is not adding optional layers around products or payments.
- Proxy was rejected because there is no access control, caching, or lazy loading problem.
- Bridge was rejected because the cart does not yet have two independent hierarchies that need to vary separately.

## Result

The client can now use `CheckoutFacade` for checkout, and payment integration no longer depends directly on the external provider's response format.
