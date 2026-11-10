# Spec: Paystack checkout

## Goal
Let customers pay for an order with Paystack.

## Users
Customers in Nigeria buying from our web store.

## Requirements
- Customer clicks Pay and is taken to Paystack.
- Order is marked paid only after Paystack confirms the payment.
- Amounts are in Naira.

## Acceptance criteria
- A paid order shows "Paid" within 1 minute of payment.
- A failed or abandoned payment leaves the order "Unpaid".
- A forged confirmation request does not mark an order paid.
