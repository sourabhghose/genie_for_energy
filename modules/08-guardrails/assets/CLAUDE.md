# genie_for_energy — Claude Code Instructions

> This file provides Claude Code-specific operating instructions for the genie_for_energy repository.
> It mirrors AGENTS.md and adds Claude Code-specific conventions.
> If both files are present, Claude Code reads CLAUDE.md preferentially.

---

## Repository purpose

**SmartGrid Analytics Platform** — energy analytics demo and training repository for a fictional Australian energy retailer (50,000 customers, 6 states).

**This is a demo and training repository.** Do not connect to live production data. Do not treat any `*_prod` catalog as expendable.

---

## Claude Code-specific conventions

### Before writing any code
1. Read the relevant existing files before proposing changes
2. Understand the current structure before modifying it
3. Search for existing implementations — do not recreate what already exists

### Change proposal format
- Always propose changes as a diff — never auto-apply
- For multi-file changes: list all affected files, get confirmation, then propose one file at a time
- For schema changes: state the impact on downstream tables before proposing

### Commit message format
```
<type>: <description>

Types: feat, fix, refactor, docs, test, chore, perf
Example: feat: add data quality checks to silver_meter_readings pipeline
```

---

## Operating environment

| Catalog | Purpose | Default? |
|---|---|---|
| `smartgrid_dev` | All development and lab work | **Yes — always default here** |
| `smartgrid_staging` | Pre-production validation | Only when explicitly requested |
| `smartgrid_prod` | Production | **Never — requires explicit double-confirmation** |

---

## Hard rules (no exceptions without explicit user override)

1. **Never push directly to `main`** — always use a PR
2. **Never use `git push --force`** on shared branches — use `git revert`
3. **Never write to `smartgrid_prod`** unless the user confirms twice in the same session
4. **Never propose `DROP TABLE`** without first checking what depends on it
5. **Never run bulk DELETE or TRUNCATE** without showing the affected row count first
6. **Never commit secrets, tokens, or connection strings** — use environment variables
7. **Never assume catalog context** — always confirm the target before any write

---

## Code quality checklist (apply to all proposals)

- [ ] Functions under 50 lines
- [ ] No `SELECT *` — always specify columns
- [ ] Three-part table naming: `catalog.schema.table`
- [ ] Data quality checks on silver-layer inputs
- [ ] Error paths explicitly handled (log, do not swallow)
- [ ] No hardcoded catalog or schema names — use config/variables
- [ ] PySpark, not pandas

---

## Domain conventions

- Energy measurements: **kWh**
- Currency: **AUD**
- Time storage: UTC; display AEST/AEDT
- Customer IDs: `CUST-XXXXXX`
- Meter IDs: `MTR-XXXXXXXX`
- Australian state codes: NSW, VIC, QLD, SA, WA, TAS

---

## Prohibited without explicit confirmation

- `DROP TABLE` / `DROP SCHEMA` / `DROP CATALOG`
- `TRUNCATE TABLE`
- `DELETE FROM` without restrictive `WHERE`
- `ALTER TABLE` removing columns
- Any write to `*_prod` catalogs
- `git push --force` on any branch
- Sending messages to external tools (Slack, Jira, email) without showing draft first

---

## Security

- No hardcoded secrets, tokens, or passwords — ever
- Validate external inputs at system boundaries
- Do not surface customer PII in query outputs or logs
- If a security issue is found: stop, flag it, fix it before continuing

---

## Useful context

The base lab is at: https://github.com/sourabhghose/genie_for_energy

Module structure:
- `guides/` — step-by-step exercise guides (00-setup through 08-guardrails)
- `modules/` — hands-on notebook implementations
- `setup/generate_energy_data.py` — synthetic dataset generation
- `dashboard/` — Lakeview dashboard template
- `AGENTS.md` — cross-agent instructions (this file's companion)

---

*This file should be kept in sync with AGENTS.md. If they diverge, resolve the conflict before the next session.*
