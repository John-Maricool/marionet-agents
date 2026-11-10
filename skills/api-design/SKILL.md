---
name: api-design
description: Conventions for designing HTTP APIs — resource naming, status codes, errors, pagination, versioning and validation. Use when designing or reviewing an API endpoint.
---

# API design

## Naming
- Plural nouns for collections: `/users`, `/users/{id}`.
- No verbs in paths; use HTTP methods.

## Status codes
- 200 OK, 201 Created (with Location header), 204 No Content.
- 400 invalid input, 401 not signed in, 403 not allowed, 404 not found, 409 conflict, 422 validation failed.
- 5xx only for server faults; never for bad input.

## Errors
Return one shape everywhere:
```json
{ "error": { "code": "validation_failed", "message": "Email is required", "field": "email" } }
```

## Pagination
Cursor-based for large or changing lists: `?limit=50&cursor=...`, response includes `next_cursor`.

## Validation
Validate every field at the boundary. Reject unknown fields on writes.

## Versioning
Prefix with `/v1`. Never break a published version; add a new one.

## Money
Store and send amounts as integers in the smallest unit (kobo, cents), with an ISO 4217 currency code.
