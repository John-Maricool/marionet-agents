---
name: owasp-checklist
description: Practical security review checklist based on the OWASP Top 10 and OWASP Mobile Top 10 categories. Use when reviewing web, mobile or API code for vulnerabilities.
---

# Security review checklist

Check high-risk paths first: authentication, payments, file upload, admin actions, anything with personal data.

## Access control
- Every endpoint checks the caller is allowed to act on that specific record (no ID swapping).
- Admin actions require admin role server-side, not just a hidden button.

## Authentication and sessions
- Passwords hashed with bcrypt, scrypt or Argon2.
- Rate limiting on login, OTP and password reset.
- Tokens expire; refresh tokens can be revoked.

## Injection and input
- Parameterised queries everywhere; no string-built SQL.
- Output encoded for its context (HTML, URL, JS).
- File uploads: type and size checked, stored outside the web root, never executed.

## Secrets and configuration
- No secrets in code, apps, logs or front-end bundles.
- Debug mode and verbose errors off in production.
- Dependencies scanned for known vulnerabilities.

## Payments and webhooks
- Webhook signatures verified (Flutterwave, Paystack, Stripe all sign webhooks).
- Amount and currency re-checked server-side against the order, never trusted from the client.
- Idempotency: the same payment event processed twice has no extra effect.

## Mobile
- Secrets in secure storage (Keychain, Keystore, flutter_secure_storage).
- No sensitive data in logs, screenshots of sensitive screens blocked where needed.
- TLS everywhere; certificate pinning considered for payment and banking apps.

## Severity
- Critical: direct loss of money, account takeover, or mass data exposure.
- High: exploitable with some effort, or exposes one user's data.
- Medium: needs unusual conditions. Low: hardening.
