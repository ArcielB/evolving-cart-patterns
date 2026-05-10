# Phase 1 AI Log - Creational Pattern

## Prompt

I asked:

> The cart currently creates physical, digital, and subscription products inside `ShoppingCart.create_product` using conditional branches. Which creational pattern is appropriate, and what problem would it solve?

## AI Response Summary

The AI suggested using either Factory Method or Simple Factory. It explained that product construction rules should be moved out of `ShoppingCart` so the cart is not responsible for knowing the creation details of every product type. It also warned that a full Abstract Factory would be unnecessary unless the project needed complete families of related objects.

## Decision

I implemented a Simple Factory named `ProductFactory`. The cart still has a convenient `add_product` method, but object creation is delegated to the factory.

## What I Accepted

- Move product creation out of `ShoppingCart`.
- Keep product creation rules in one named class.
- Add tests that verify the factory creates known product types and rejects unknown ones.

## What I Rejected

- I rejected Abstract Factory because this project does not create complete product families.
- I rejected Singleton because a product factory does not need global shared state.

## Result

The creation-related problem from `PROBLEMS.md` is reduced: adding or changing product construction rules is now isolated in `ProductFactory` instead of being mixed with cart behavior.
