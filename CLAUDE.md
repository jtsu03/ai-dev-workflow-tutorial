# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **documentation-only tutorial repository** — there is no application code, build system, tests, or CI/CD. The content teaches an AI-assisted professional development workflow using a hands-on project: building and deploying an e-commerce sales dashboard.

## Structure

- `v2/` — Current tutorial format (async pre-work + 3-hour live workshop). This is the primary content.
  - `pre-work-setup.md` — Account creation and tool installation guide (~60-90 min async)
  - `workshop-build-deploy.md` — Live workshop guide covering spec-kit → Jira → build → deploy
- `v1/` — Original two-session format, kept as reference material
- `prd/ecommerce-analytics.md` — The sample PRD students use as their starting point
- `data/sales-data.csv` — Sample dataset (~1,000 rows) for the dashboard project

## Workflow Being Taught

The tutorial teaches this development cycle:

1. **Spec-Kit** — Transform a PRD into a constitution, specification, and implementation plan
2. **Jira** — Generate and track tasks from the implementation plan (via Atlassian MCP Server)
3. **Cursor + Claude Code** — Implement each Jira issue, one at a time
4. **Git** — Commit after each issue with a message referencing the Jira ticket
5. **Streamlit Cloud** — Deploy from the GitHub repo's `main` branch

The stack for the student's project: Python 3.11+, `uv` (package manager), Streamlit, Plotly, Pandas.

## Editing Guidelines

- The tutorial UI instructions (GitHub, Atlassian, Cursor, Claude interfaces) evolve frequently — add a note like *"Note: UI may look slightly different than shown"* rather than writing hyper-specific click-by-click instructions that will go stale.
- `v2/` is the source of truth for current workflow. `v1/` is legacy — avoid making changes there unless explicitly asked.
- The PRD in `prd/ecommerce-analytics.md` is intentionally stable — it's the student artifact. Don't modify it unless the tutorial requirements change.
- The sample data in `data/sales-data.csv` produces ~$650K-$700K total sales across 482 orders. If the data is regenerated, verify these totals match the workshop's verification checklist.
