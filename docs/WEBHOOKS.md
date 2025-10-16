# Webhooks

- Endpoint: /payments/webhook/
- Security: HMAC signature + timestamp window
- Dedupe: WebhookEvent.dedupe_key unique
- Retry: exponential backoff on 5xx, alert on 4xx

