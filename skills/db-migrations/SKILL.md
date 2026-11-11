---
name: db-migrations
description: Safe database migration patterns — expand and contract, backfills, indexes without downtime, and rollback plans. Use when writing or reviewing any schema change.
---

# Safe database migrations

## Expand, migrate, contract
1. **Expand:** add new columns or tables; nullable or with a default. Old code keeps working.
2. **Migrate:** deploy code that writes to both; backfill old rows in batches.
3. **Contract:** in a later release, once nothing reads the old shape, remove it.

Never rename or drop in the same release that stops using a column.

## Backfills
- Batch by primary key (for example 1,000-10,000 rows per batch), with a pause between batches.
- Make the backfill re-runnable (idempotent).
- Run it as a separate job, not inside the schema migration.

## Indexes
- PostgreSQL: `CREATE INDEX CONCURRENTLY` (outside a transaction) on large tables.
- MySQL: check the engine supports online DDL for the change.

## Locks
Adding a NOT NULL column with a volatile default, changing a column type, or adding a foreign key can lock or rewrite a table. On large tables, add the constraint as NOT VALID and validate separately where the database supports it.

## Data types
- Money: integer in the smallest unit (kobo, cents) plus an ISO 4217 currency code.
- Timestamps: with time zone, stored in UTC.

## Rollback
Every migration has a down step or a written recovery plan. Test both directions on a copy before review.
