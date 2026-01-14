# ADR-001 — E2E Test Framework (QA)
## Context
We need to select automation framework for our end-to-end (E2E) testing pipeline. This framework will be integral to our CI/CD processes, running tests that simulate real user interactions on our platform.
Our team works with TypeScript and Python, and the ability to write tests in these languages is essential. EAP requires reliable end-to-end coverage for:
- multirole flows (Requester/Approver/Admin)
- workflow state transitions and routing
- dashboards with tables/forms
- audit trail evidence and notifications

The QA repo must integrate with GitHub Actions, producing artifacts for debugging failures.

## Decision
Use **Playwright + Pytest** as the E2E automation framework.

### Key conventions
#### Project layout (in eap-qa)
- `e2e-tests/` contains E2E tests and Page Objects
- `docs/` contains QA documentation and ADRs

#### Test grouping and markers
- `@pytest.mark.smoke` — fast, PR-gate subset
- `@pytest.mark.regression` — stable nightly suite
- Requirement mapping markers: `@pytest.mark.FR_RM_003` (or similar consistent convention)

#### Selector strategy
- Prefer `data-testid` attributes for all critical controls (forms, buttons, table actions)
- Avoid brittle selectors (deep CSS, text-only selectors) unless necessary
- Frontend uses Ant Design; agree on stable test IDs at component boundaries

#### Artifacts and reporting
- On failure: store screenshot + Playwright trace
- Generate an HTML test report and upload artifacts in CI

## Consequences
### Positive
- Strong debugging (trace viewer), stable waiting model
- Fits Python QA stack and integrates well with Pytest plugins
- Works cleanly in GitHub Actions + Docker

### Negative / trade-offs
- UI tests are slower than API tests; must keep PR gate small
- Requires team discipline on selectors and test data isolation

## Alternatives considered
- Selenium: more boilerplate, weaker trace artifacts, slower stabilization
- Cypress: good UI tooling but diverges from Python QA stack

## Implementation notes
- Standard CI command:
  - `pytest -m "smoke" --tracing=retain-on-failure`
- Browser install and artifact upload handled in GitHub Actions 