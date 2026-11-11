---
name: data-quality
description: Data quality checks and practices for pipelines and datasets — completeness, uniqueness, validity, freshness, leakage and personal data handling. Use when building pipelines or preparing datasets.
---

# Data quality

## Checks on every table or dataset
| Check | Example |
|---|---|
| Row count | Within expected range vs. yesterday |
| Completeness | Required columns not null |
| Uniqueness | Primary keys unique; no duplicate records |
| Validity | Values in allowed ranges and formats (amounts >= 0, valid dates, known categories) |
| Freshness | Latest record newer than the schedule allows |
| Consistency | Foreign keys match; totals reconcile with source |

Fail loudly: a failed check stops downstream jobs and alerts someone.

## For ML datasets
- Look for leakage: features that contain the answer, or the same user in train and test.
- Check label balance and label noise on a sample.
- Keep a fixed, versioned held-out test set.

## Personal data
- Collect and copy only what is needed.
- Hash or pseudonymise identifiers that are only used for joining.
- Keep personal data inside approved systems.

## Documentation
Every table: owner, source, refresh schedule, column meanings, known issues.
