# Evolving Cart Patterns

**Student:** Arciel Aliognis Baez Zamora  
**Student number:** 221229078  
**Selected topic:** D - E-Commerce Cart

I selected the e-commerce cart because it naturally becomes hard to maintain when product creation, discounts, payment selection, and checkout rules are placed in the same class. This topic is a good fit for showing why design patterns matter: each phase removes one concrete source of change pressure from the original cart.

## Project

This repository is a design patterns homework project. It starts with an intentionally flawed cart implementation and then evolves through creational, structural, and behavioral design patterns.

Phase 0 currently keeps too much responsibility inside `ShoppingCart` on purpose. Later branches refactor this baseline step by step.

## Current Behavior

- Add physical, digital, or subscription products to a cart.
- Remove all or part of a product quantity.
- Calculate cart subtotal.
- Checkout with hard-coded discount and payment conditionals.

## Run

```bash
python3 -m pip install -e .
python3 -m pytest
```

## Repository Workflow

- `main`: Phase 0 baseline and final merged result.
- `phase-1`: Creational pattern work.
- `phase-2`: Structural pattern work.
- `phase-3`: Behavioral pattern work and CI.

## Diagrams

The initial Phase 0 UML diagram is in `docs/diagrams/phase0-before.mmd`.
