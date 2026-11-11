---
name: deploy-checklist
description: Pre-deploy, deploy and post-deploy checklist for web services and mobile app releases, including rollback. Use when planning or running any production release.
---

# Deploy checklist

## Before
- [ ] Change is merged, CI is green, and the version is tagged.
- [ ] Migrations reviewed; expand-only, or a maintenance window is approved.
- [ ] Rollback steps written and tested on staging.
- [ ] Feature flags in place for risky changes.
- [ ] Someone is available to watch for at least 30 minutes after.
- [ ] Human approval recorded.

## During
- Deploy to staging, run smoke tests, then production.
- Use gradual rollout where possible (canary, percentage, or staged store rollout).

## After
- [ ] Health checks green; error rate and latency normal.
- [ ] Key flows checked by hand (sign-in, payment, main feature).
- [ ] Result recorded in the deploy log.

## Mobile releases
- Upload to internal or closed testing first.
- Use staged rollout on Google Play (for example 10%, then 50%, then 100%).
- Watch crash-free rate before increasing the rollout.
- Store review times vary; never promise a same-day release to a client.

## Rollback triggers
Roll back without debate if error rate or crash rate clearly rises, payments fail, or sign-in fails.
