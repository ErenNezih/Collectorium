# Payments Design (Sandbox Iyzico)

- Abstraction: provider-agnostic service with Iyzico adapter
- State machine: initiated -> authorized -> captured -> refunded/failed
- Idempotency: PaymentTransaction.idempotency_key unique
- Totals contract: Decimal, ROUND_HALF_UP, price_snapshot
- Capture policy: FEATURE_PAYMENTS_CAPTURE_IMMEDIATE

