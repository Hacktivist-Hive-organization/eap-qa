# Regression Test Plan for EAP
## 1. Purpose
Regression testing ensures that core EAP flows still works after code changes. Because planning is not finalized, this plan defines the initial regression approach focuses on core must-not-break flows driven by P0/P1 requirements.

## 2. Regression scope
### 2.1 Smoke suite (PR gate)
Covers the minimum “system is usable” checks:
 - Login/logout
 - RBAC basic (Requester cannot access Admin/Approver pages; Admin can access all)
 - Create request → submit 
 - Request auto-routed to default approver
 - Approver: under review → approve OR reject
 - Admin: approved → in progress → completed
 - Audit log entry exists for key actions
 - Notification triggered or failure logged

### 2.2 Core regression suite (nightly)
Run daily or before a release:
 - Request validation (required fields, max lengths)
 - Status transitions rules (allowed + blocked transitions)
 - Dashboards show correct items
 - Approver rejection requires reason 
 - Permissions on request details
 - Email notifications for key events (submitted/approved/rejected/completed)
 - Audit logging for key events (login, status change, approvals, admin changes)

## 3. Suite selection rules
A test qualifies for regression if:
- deterministic data
- stable selectors
- runtime acceptable for schedule


## 4. When regression runs
Aligned with GitHub Actions:
- scheduled (every 4 hours) workflows on main
- pre-demo / pre-release run
- after major dependency or infrastructure changes


## 5. Reporting
Artifacts stored per run:
- HTML report
- screenshots + traces for failures
- summary of suite results and duration