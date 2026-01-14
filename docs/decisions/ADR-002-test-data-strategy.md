# ADR-002 — Test Data Strategy (QA)

## Context
EAP is a workflow-driven system with role-based actions and state transitions.
Unstable tests usually come from:
 - Shared mutable data
 - Tests depending on execution order
 - Reusing the same requests across tests

The backend uses PostgresSQL + SQLAlchemy, and CI runs in isolated GitHub Actions environments, which allows controlled and repeatable test data setup.

## Decision
Use simple, deterministic, and isolated test data with a small seeded baseline and test-owned data.

### A. Baseline Seed Data
Seed once per environment (or per CI run):
- roles: Requester, Approver, Admin
- request types/subtypes
- default approver mapping per request type
- a small set of test users per role (or ability to create via API)

This seed must be safe to run repeatedly and must not be modified by tests.

### C. Isolation model
To be defined.

### D. Role-based users
- Provide per-role credentials:
  - requester_*
  - approver_*
  - admin_*
- JWT expiry considerations:
  - E2E tests should re-authenticate when token expired rather than relying on long sessions. :contentReference[oaicite:32]{index=32}

## Consequences
### Positive
- Repeatable CI outcomes
- Easier debugging and stable regression suites

### Negative
- Requires seed scripts/endpoints and disciplined test builders
