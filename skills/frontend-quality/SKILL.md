---
name: frontend-quality
description: Checklist for web front-end code covering UI states, accessibility, performance and security. Use when building or reviewing web UI.
---

# Front-end quality checklist

## States
Every view handles: loading, empty, error, success, and no permission. Forms show inline validation and a server-error message, and disable submit while sending.

## Accessibility
- Semantic elements (`button`, `nav`, `main`, `label`), not clickable `div`s.
- Every input has a label; every image has alt text (empty alt if decorative).
- Everything works with the keyboard; focus is visible and moves sensibly in dialogs.
- Text contrast at least 4.5:1.

## Performance
- Images sized and lazy-loaded; modern formats where supported.
- No large library imported for a small job.
- Lists over about 100 items are paginated or virtualised.
- Avoid layout shift: reserve space for images and async content.

## Security
- No secrets in front-end code or environment variables shipped to the browser.
- Never inject unsanitised user HTML.
- Auth tokens in httpOnly cookies where the backend supports it.

## Tests
Cover validation rules and the main user flow; avoid testing implementation details.
