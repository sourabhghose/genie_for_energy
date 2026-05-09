# genie_for_energy — AI Agent Instructions

> This file is read automatically by AI coding assistants (Genie Code, Claude Code, GitHub Copilot, etc.)
> when working in this repository. It defines the operating rules for AI-assisted development.

---

## Repository purpose

**SmartGrid Analytics Platform** — energy analytics lab for a fictional Australian energy retailer with 50,000 customers across 6 states.

This is a **demo and training repository**. It is used for hands-on workshops and field engineering demos. Do not treat it as a production system. Do not connect it to live production data sources without explicit authorization.

---

## Branch rules

- **Always work on a feature branch** — never commit directly to `main`
- Branch naming convention: `feature/<short-description>`, `fix/<short-description>`, `chore/<short-description>`
- Before deleting a branch, confirm it has been merged and the merge commit is validated
- **Never propose `git push --force`** on `main` or any protected branch
- For rollbacks: propose `git revert` (creates a new commit) — not force-push or `git reset --hard`
- All changes to `main` require a pull request with at least one reviewer

---

## Catalog and schema rules

| Environment | Catalog | Use |
|---|---|---|
| Development | `smartgrid_dev` | All hands-on lab work |
| Staging | `smartgrid_staging` | Pre-production validation |
| Production | `smartgrid_prod` | **Requires explicit confirmation — never default to this** |

- **Never write to `smartgrid_prod` without explicit user confirmation** in the current session
- When catalog is not specified, default to `smartgrid_dev`
- Table naming must respect medallion layers:
  - `bronze_*` — raw ingested data
  - `silver_*` — cleansed and validated data  
  - `gold_*` — curated, business-ready data
- Always use three-part naming: `catalog.schema.table`
- Do not use `SELECT *` — always specify columns

## FE workspace resource lifecycle (e2-demo-field-eng)

When working in the shared `e2-demo-field-eng` workspace, all resources are subject to automated cleanup:

- **Catalogs without a `RemoveAfter` tag are deleted after 14 days** — always add this tag when creating a catalog
  - Format: `RemoveAfter = YYYY-MM-DD` (max 1 year from today)
  - Use `YYYYMMDD` format in Unity Catalog if hyphens are not allowed
- Resources named `tmp_*` or `test_*` are deleted weekly — do not use these prefixes for lab data
- All personal content must be under `/Users/[your.email@databricks.com]` — not at workspace root
- Do not create resources in shared locations without using permissions to control access

---

## Data domain conventions

- All energy measurements: **kWh**
- All currency: **AUD**
- Customer IDs follow the pattern: `CUST-XXXXXX`
- Meter IDs follow the pattern: `MTR-XXXXXXXX`
- State codes: NSW, VIC, QLD, SA, WA, TAS (Australian states only)
- Date/time: always store in UTC, display in AEST/AEDT
- Regulatory references: AEMO (market operator), AER (economic regulator)

---

## Code style

- **PySpark, not pandas** — this is a distributed data platform
- Use Delta Lake format for all managed tables
- Add `# Data quality check` comments above any validation logic
- All silver-layer transformations must include explicit null handling
- Error handling: log with full context, do not silently swallow exceptions
- No hardcoded catalog/schema names — use variables or config

---

## Prohibited actions — require explicit second confirmation

Before proposing any of the following, state clearly that the action is irreversible and require the user to confirm explicitly:

- `DROP TABLE`, `DROP SCHEMA`, `DROP CATALOG`
- `TRUNCATE TABLE`
- `DELETE FROM` without a restrictive `WHERE` clause
- `ALTER TABLE` that removes columns
- Any write operation to `smartgrid_prod`
- Force-push to any branch
- Deleting any branch

---

## What you should NOT do

- Do not assume catalog context — always confirm target before any write
- Do not run code automatically — propose first, wait for approval
- Do not create new catalogs or schemas without explicit instruction
- Do not access tables outside the `smartgrid_*` catalog family without explicit instruction
- Do not send messages to external systems (Slack, email, Jira) without showing a draft first

---

## What you SHOULD do

- Read existing code before proposing changes — understand before modifying
- Propose one change at a time for review — no bulk modifications without per-file approval
- Flag any operation that cannot be reversed before proposing it
- Use the `smartgrid_dev` catalog by default
- Include data quality checks in all silver-layer pipelines

---

## Quick reference: key tables

| Table | Layer | Description |
|---|---|---|
| `bronze_*.raw_customers` | Bronze | 50K customer records, 6 Australian states |
| `bronze_*.raw_meter_readings` | Bronze | 10.7M hourly readings, Jan–Mar 2025 |
| `bronze_*.raw_billing` | Bronze | 600K billing records, 12-month cycles |
| `bronze_*.raw_weather` | Bronze | Daily weather by state |
| `bronze_*.raw_equipment` | Bronze | Grid equipment and failure history |
| `bronze_*.raw_outages` | Bronze | 5K outage events with geospatial data |
| `bronze_*.raw_demand_response` | Bronze | 20K demand-response program records |

---

*Last updated: see git log. This file should be reviewed and updated when the repository purpose or operating environment changes.*
