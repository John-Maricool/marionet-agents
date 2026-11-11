---
name: flutter-quality
description: Senior-level quality checklist for Flutter/Dart code covering correctness, security, architecture, performance and reliability. Use when writing or reviewing Flutter code, especially code that handles money, identity or location.
---

# Flutter quality checklist

Check in this order. Report each finding as Critical, High, Medium or Low, with file:line and the fix.

## 1. Correctness
- Null-safety misuse (`!` on values that can be null).
- Unhandled async errors; `await` missing; futures fired and forgotten.
- Race conditions (two requests updating the same state).
- Lifecycle leaks: controllers, streams, timers and WebSocket subscriptions not disposed.
- `BuildContext` used after an `await` without a `mounted` check.

## 2. Security
- Tokens or keys in code or logs.
- Secrets in shared preferences instead of `flutter_secure_storage`.
- No certificate pinning on payment APIs where the risk justifies it.
- Sensitive data in logs or crash reports.
- No screenshot protection on sensitive screens (balances, PINs, ID documents).
- Payment buttons that allow double submission.

## 3. Architecture
- Layers respected: presentation, domain, data.
- No business logic in widgets.
- Repositories behind interfaces so they can be faked in tests.
- One state management approach, used consistently.

## 4. Performance
- Unnecessary rebuilds (state too high in the tree, missing selectors).
- Heavy work on the UI thread (parsing large JSON: use `compute` or isolates).
- Missing `const` constructors.
- Unpaginated lists; `ListView` without `.builder` for long lists.
- Large images not cached or resized.

## 5. Reliability
- Timeouts and retries with backoff on network calls.
- Offline, error and empty states on every screen.
- Idempotency keys on transactions.
- Reconnect logic on WebSockets.

## 6. Maintainability
- Clear naming, small files, no duplicated logic.
- Tests for business logic.
- Style issues: name the lint rule instead of nitpicking.

## Verdict
Ship / Ship after fixes / Needs rework. Any Critical finding means Needs rework.
