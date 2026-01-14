# Test Strategy for Enterprise Application Portal (EAP)
***
##### Table of Contents  
1. [Purpose](#purpose)
2. [Testing Scope](#testing-scope)
3. [Testing Approach](#testing-approach) 
4. [Environments](#environments)
5. [Tools](#tools)
6. [Test data strategy (summary)](#test-data-strategy-summary)
7. [CI quality gates](#ci-quality-gates)


***
### Purpose
<a name="purpose"></a>

The purpose of the document is to create a shared understanding of the overall goals, testing approach, tools and timings of testing activities that can be followed to ensure delivery of the product with predictable behaviour, performance and quality.
This strategy sets testing approach, scope, environments, tooling, and CI quality gates to meet MVP goals for EAP.

The test strategy guides us through common obstacles with a clear view of how to evaluate the system. Testing starts with exploration of the user stories and what the stakeholders really wants by elaborating the user stories from different perspectives.
***
### Testing Scope
<a name="testing-scope"></a>

Primary automated coverage targets are P0(Critical) and selected P1(High) requirements (auth/RBAC, request lifecycle, approval workflow, notifications, audit trail).

#### In Scope:
 - Authentication and role-based access control (Requester, Approver, Admin)
 - Request submission and status lifecycle
 - Approval routing (per request type)
 - Email notifications for key events
 - Admin/reporting dashboards
 - Immutable audit trail and request history timeline

#### Out of Scope:
 - Multi-level approvals - Only single approver per request (not chain of approvals)
 - Budget tracking - No integration with financial systems
 - Asset inventory - No tracking of physical assets after fulfillment
 - SLA management - No automatic escalation based on time
 - Advanced workflows - No conditional routing based on request details
 - Mobile apps - Web only (responsive design, not native apps)
 - Integrations - No integration with external systems (Slack, JIRA, etc.)
 - Real-time chat - No in-app messaging between users
 - Approval delegation - Approvers cannot delegate to others
 - Recurring requests - No templates for repeated requests
***
### Testing Approach
<a name="testing-approach"></a>

| Level          | Primary goal                  | Examples                                                  | Typical owner |
|----------------|-------------------------------|-----------------------------------------------------------|---------------|
| Unit           | validate isolated logic       | validators, state transition rules, permission checks     | Dev           |
| Integration    | verify service + DB behavior  | endpoints, auth, RBAC, workflow transitions, audit writes | Dev           |
| E2E API        | verify service + DB behavior  | endpoints, auth, RBAC, workflow transitions, audit writes | QA            |
| E2E UI         | verify user journeys          | submit → route → approve/reject → fulfill; dashboard UX   | QA            |
| Non-functional | checks how well app functions | performance and load tests, basic security checks         | QA + DevOps   |


#### Unit Tests
Unit tests are to provide confidence about specific implementations of logic that could be harder to test at the service level, or to verify specific exceptional behaviour that is difficult or time-consuming to produce at the service level.

#### Integration Tests
Integration test is to test whether many separately developed modules work together as expected. It was performed by activating many modules and running higher level tests against all of them to ensure they operated together. They have the advantage of giving you the confidence that your application can correctly work with all the external parts it needs to talk to. Unit tests can't help you with that.

Since we have end-to-end api tests complementary for integration tests, we can validate collaboration between a small number of internal components and can keep the scope narrow at this level.
#### End-to-End Test
End-to-end testing is the type of test that connects all the business processes that are in scope for your project. It defines the product’s system dependencies and ensures all integrated pieces work together as expected.

User Interface end-to-end tests allow us to automate our tests by automatically driving a browser against deployed services. While end-to-end api tests avoids graphical user interface when testing application and validates complete API workflows across components/services as a deployed system.

#### Performance Test
Performance test is a critical process in software testing that evaluates an application’s speed, responsiveness, and stability under various conditions.

Load testing is a type of performance testing conducted to evaluate the behavior of a component or system under varying loads, usually between anticipated conditions of low, typical, and
peak usage. Stress testing is a type of performance testing conducted to evaluate a system or component at or beyond the limits of its anticipated or specified workloads, or with reduced availability of resources such as access to memory or servers.

The system is expected to meet the following baseline performance criteria:
 - ***Page load time:*** Critical pages load in under 2 seconds
 - ***Form submission response time:*** Request creation, submission, approval, and rejection actions return a response in under 1 second
 - ***Concurrency:*** The system supports 100 concurrent users performing typical actions without significant degradation
 - ***Database efficiency:*** Database queries are optimized to handle large datasets without excessive latency
***
### Environments
<a name="environments"></a>
- **Local dev (Docker Compose):** fast iteration, optional email mock
- **CI ephemeral (Docker):** deterministic seeded data; isolated per workflow run
- **Prod-like (VPS):** production-like settings; limited scheduled regression

***
### Tools
<a name="tools"></a>
Performance tools selection is documented as “recommended”, not mandatory for early MVP.
- **Pytest** for test runner and assertions
- **Playwright (sync)** for E2E tests
- **Playwright traces/screenshots** for failed E2E tests
- **pytest-html** for reporting, allure report also possible later
- **Load and Stress test:** start with k6 or Locust
- **CI/CD Integration:** GitHub Actions 

***
### Test data strategy (summary)
<a name="test_data_strategy"></a>

Full policy is defined in ADR-002-test-data-strategy.md.
- sensitive credentials handled using environment variables
- seeding test data
- test data stored in JSON

***
### CI quality gates
<a name="CI-quality-gates"></a>
Aligned with GitHub Actions + Docker.
#### PR checks (fast feedback)
- Unit tests (backend/frontend)
- API smoke (auth etc.)
- Optional E2E smoke (login + “create draft” or “submit request”)
