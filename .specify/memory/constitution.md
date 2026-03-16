<!--
SYNC IMPACT REPORT
==================
Version change: N/A (initial) → 1.0.0
Modified principles: N/A (first population of template)
Added sections:
  - Core Principles (I–V)
  - Technology Stack
  - Development Workflow
  - Governance
Removed sections: None
Templates reviewed:
  - .specify/templates/plan-template.md ✅ aligned (Constitution Check gate present)
  - .specify/templates/spec-template.md ✅ aligned (user stories, acceptance scenarios, measurable outcomes)
  - .specify/templates/tasks-template.md ✅ aligned (unit + integration test phases present)
Deferred TODOs:
  - RATIFICATION_DATE set to today (2026-03-16); update if original adoption date differs.
  - Cloud platform vendor (AWS / GCP / Azure) not specified — annotated in Principle V.
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Data Integrity First (NON-NEGOTIABLE)

The dashboard MUST display accurate, up-to-date data at all times. Stale, incorrect, or
unvalidated metrics MUST NOT be presented to any user — whether non-technical or analyst.

- All data ingested from external APIs MUST be validated before rendering.
- Calculations and aggregations MUST have deterministic, tested logic.
- If live data is unavailable, the dashboard MUST surface a clear error state rather than
  showing cached or placeholder values silently.
- Data freshness timestamps MUST be visible to users wherever metrics are displayed.

**Rationale**: Both audience segments (non-technical viewers and analysts) make business
decisions from this dashboard. An incorrect number is worse than no number.

### II. Dual-Audience Design

Every UI surface MUST serve both non-technical business users and analytical power users
without requiring separate codebases or views.

- High-level KPI summaries MUST be prominently placed and require no domain knowledge to
  interpret.
- Drill-down views and raw data access MUST be available but MUST NOT clutter the primary
  view.
- Labels, axes, and tooltips MUST use plain business language (e.g., "Total Revenue" not
  "sum(order_value)").

**Rationale**: A single dashboard serving mixed audiences eliminates sync issues between
reporting tools and ensures a shared source of truth.

### III. API-First Data Access

All sales data MUST be sourced from live or near-real-time external APIs. Static file
ingestion is permitted only for local development or testing fixtures.

- API clients MUST be implemented as isolated, independently testable modules.
- API contracts (endpoints, schemas, auth) MUST be documented in `specs/contracts/`.
- API failures MUST be handled gracefully; the dashboard MUST degrade predictably (see
  Principle I).

**Rationale**: Real-time API feeds are the chosen data source. Tight coupling to static
files would undermine data freshness guarantees.

### IV. Test-Verified Data Pipelines

All data transformation logic and API integration code MUST be covered by both unit tests
and integration tests before shipping.

- Unit tests MUST cover every data transformation, aggregation, and formatting function.
- Integration tests MUST exercise the full data pipeline from API call through to rendered
  metric, using real or realistic API responses (not mocked schemas).
- Tests MUST be run and pass in CI before any merge to the main branch.
- New API endpoints or transformed fields added to the dashboard MUST have corresponding
  tests before the feature is considered complete.

**Rationale**: Data pipelines are the highest-risk layer in this system. Unit tests alone
are insufficient because mock/real divergence can mask broken integrations (lesson from
common production incidents).

### V. Cloud-Native Deployment

The dashboard MUST be deployable to a cloud platform (AWS, GCP, or Azure) using
containerized or serverless packaging.

- The application MUST be stateless; all state lives in external APIs or storage services.
- Environment-specific configuration (API keys, endpoints) MUST be injected via environment
  variables — never hardcoded.
- The deployment artifact (container image or serverless package) MUST be reproducible from
  the repository without manual steps beyond environment variable injection.

**Rationale**: Cloud-native deployment enables scalability, managed infrastructure, and
team-agnostic operations. The specific cloud vendor (AWS/GCP/Azure) is not mandated by this
constitution and SHOULD be decided per deployment environment.

## Technology Stack

- **Language**: Python 3.11+
- **UI Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Package Manager**: `uv`
- **Testing**: pytest (unit), pytest + live API fixtures (integration)
- **Deployment**: Containerized (Docker) targeting a cloud platform

All technology choices MUST align with this stack. Deviations require a justified entry in
the Complexity Tracking table of the feature's `plan.md`.

## Development Workflow

1. **Specify** — Every feature begins with a spec (`/speckit.specify`) derived from the PRD.
2. **Plan** — Implementation design produced via `/speckit.plan`; Constitution Check MUST
   pass before Phase 0 research proceeds.
3. **Tasks** — Actionable task list generated via `/speckit.tasks`; tasks MUST be organized
   by user story to enable independent implementation and testing.
4. **Implement** — One Jira issue at a time; commit after each with a message referencing
   the ticket.
5. **Test** — Unit and integration tests MUST pass locally before pushing.
6. **Deploy** — Merge to `main` triggers cloud deployment pipeline.

## Governance

- This constitution supersedes all other development practices and style guides within this
  project.
- Amendments MUST be documented with a version bump (see versioning policy below), a summary
  of the change, and a migration note if existing features are affected.
- All pull requests MUST include a Constitution Check confirming no principles are violated.
  Violations require a justified Complexity Tracking entry in the feature's `plan.md`.
- Versioning policy:
  - **MAJOR**: Backward-incompatible principle removal or redefinition.
  - **MINOR**: New principle or section added, or materially expanded guidance.
  - **PATCH**: Clarifications, wording, or non-semantic refinements.
- Compliance review: conduct a full constitution review at the start of each major feature
  cycle to ensure principles remain relevant.

**Version**: 1.0.0 | **Ratified**: 2026-03-16 | **Last Amended**: 2026-03-16
