---
name: design-system-basics
description: Design system and accessibility basics — tokens, components and states, contrast, touch targets, mobile-first and low-bandwidth design. Use when designing any screen, component or visual.
---

# Design system basics

## Tokens
Define once, use everywhere: colour (brand, surface, text, accent, error, success), type scale, spacing (4 or 8 px steps), radius, elevation. Name by role (`color.text.primary`), not by value (`gray-900`).

## Components and states
Every interactive component: default, hover or pressed, focused, disabled, loading, error. Every screen: empty, loading, error, success, offline, no permission.

## Accessibility
- Body text contrast at least 4.5:1; large text at least 3:1.
- Touch targets at least 44×44 pt (iOS) or 48×48 dp (Android).
- Never use colour alone to show meaning; add text or icons.
- Support system font scaling.

## Mobile-first, real conditions
- Design for small, low-end Android phones first.
- Assume slow or intermittent networks: skeletons, offline states, small images.
- Keep forms short; use the right keyboard type.

## Handoff
Name components and tokens exactly as developers will use them. List every state. Note anything that differs between iOS and Android.

## Ethics
No dark patterns: no hidden fees, forced continuity, confirmshaming or disguised ads.
