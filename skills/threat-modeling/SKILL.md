---
name: threat-modeling
description: Lightweight threat modeling using STRIDE for features and systems. Use when designing a new feature or system that handles money, identity, location or personal data.
---

# Threat modeling (STRIDE, lightweight)

1. **Draw the system:** components, data stores, external services, and the trust boundaries between them (device to API, API to payment provider, staff to admin panel).
2. **List assets:** money, credentials, personal data, location, business data.
3. **For each data flow across a boundary, ask STRIDE:**
   - **S**poofing: can someone pretend to be another user or service?
   - **T**ampering: can data be changed in transit or at rest?
   - **R**epudiation: can someone deny an action because it is not logged?
   - **I**nformation disclosure: can data leak?
   - **D**enial of service: can someone make it unavailable cheaply?
   - **E**levation of privilege: can a user gain rights they should not have?
4. **Rate** each threat (impact × likelihood) and **mitigate** the high ones.
5. **Record** open risks the business is accepting, and who accepted them.

Keep it to one page for a feature. Update it when the design changes.
