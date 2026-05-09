# Genie Code Workspace Instructions

> **Two versions in this file:**
> - **Part 1:** FE Demo Workspace instructions — adapted from the real `e2-demo-field-eng` governance policy. Use this when running the lab in the shared FE workspace.
> - **Part 2:** SmartGrid template — a generic template for enterprise/customer workshops. Adapt for your customer's environment.

---

## Part 1: FE Demo Workspace Instructions (e2-demo-field-eng)

> Use this block when running the Genie for Energy lab in the shared `e2-demo-field-eng` workspace.
> Based on the Field Engineering Shared Workspace Use and Retention Policy.

---

### Operating context

You are operating in the Databricks Field Engineering shared demo workspace (`e2-demo-field-eng`). This is a **shared environment used by many Field Engineers** for demos, training, and testing. Your actions can affect other users. Treat all resources as shared, ephemeral, and subject to automated cleanup.

**Critical:** Do not store customer data, PII, or GDPR-regulated data in this workspace under any circumstances.

### Resource lifecycle — what gets deleted automatically

You must understand these cleanup rules before creating any resource:

| Resource | Deleted when |
|---|---|
| Catalogs (no `RemoveAfter` tag) | 14 days after creation |
| `tmp_` / `test_` prefixed resources | Weekly |
| Saved queries not run in 180+ days | Automated cleanup |
| SQL warehouses inactive 24+ hours | Deleted |
| Clusters running 8+ hours | Killed daily |
| GPU clusters / endpoints | Killed daily |
| Genie Spaces (last updated 30+ days) | Deleted |
| Databricks Apps (stopped, 7+ days since update) | Deleted |
| Jobs older than 30 days (no `RemoveAfter` tag) | Deleted |
| DLT pipelines not updated in 90+ days | Deleted |
| Secret scopes older than 365 days | Deleted |

**Before creating any catalog, cluster, or long-lived resource:**
- Add a `RemoveAfter` tag with format `YYYY-MM-DD` (max 1 year from today)
- If no tag is added, assume the resource will be deleted within 14 days

### Naming conventions

- All resources must have a **descriptive name** — resources named "Test", "Demo", "Untitled" will be removed
- Use `tmp_` or `test_` prefix only for resources you intend to clean up within a week
- All personal content belongs under your `/Users/[your.email@databricks.com]` folder
- Do not create resources at the workspace root level

### Catalog guidance

- Use the **Users catalog** (`users.[your_schema]`) for personal work — this will not be auto-deleted
- For any other catalog: add a `RemoveAfter` tag immediately after creation
- Always use three-part naming: `catalog.schema.table`
- Never store customer PII or GDPR data in any catalog in this workspace

### Compute guidance

- **Use shared clusters first** — there are shared clusters available in US, EMEA, and APJ regions
- If you must create your own cluster:
  - Use personal compute policy
  - Single-node by default unless you have a specific reason
  - Auto-terminate must be set to **less than 1 hour**
- Never attach libraries to shared clusters — use user-level pip installs or personal compute
- SQL warehouses: use the shared serverless endpoint (`Shared Serverless`) or `dbdemos-shared-endpoint` first
- Do not start new clusters or warehouses without confirming the user wants to incur compute cost

### Data privacy (hard rule)

- **Never generate, store, or process customer PII or GDPR-regulated data** in this workspace
- Do not save real customer data — use only synthetic or anonymised datasets
- The SmartGrid lab uses entirely synthetic data — keep it that way
- If a user asks to load external data, ask about its classification before proceeding

### Secrets and credentials

- Never suggest storing secrets in notebooks, files, or repositories in plain text
- Always use Databricks Secret Manager (`dbutils.secrets.get`) or environment variables
- Do not create service principals without the owner's username in the name

### Review requirements

- **Propose changes before executing** — never auto-run code that modifies data or schema
- For any `DROP`, `TRUNCATE`, `DELETE`, or `INSERT OVERWRITE`: pause and require explicit confirmation
- For bulk operations: list all affected resources, confirm the `RemoveAfter` tag status, then proceed one at a time
- Highlight any irreversible operation and any resource that does not have a `RemoveAfter` tag

### Approved MCP connections (FE workspace)

- **GitHub**: approved — read/write on connected repos
- **Glean**: approved — read-only knowledge lookup
- **Atlassian**: approved — read-only (Confluence/Jira lookup)
- All other MCP connections: ask before using

### Reminders

- You are operating with the user's own Databricks identity. You do not have elevated access.
- These instructions reduce accidental mistakes. They do not replace workspace permissions.
- Verbose audit logs are always enabled in this workspace — all actions are logged.
- If uncertain about intent, ask a clarifying question before proceeding.

---

## Part 2: SmartGrid Template (for enterprise/customer workshops)

> Adapt this block for a customer's own workspace. Replace placeholders as indicated.

---

### Identity and operating context

You are operating in the SmartGrid Analytics workspace for [Company Name], an energy analytics environment supporting grid operations, customer intelligence, and regulatory reporting.

This workspace connects to both development and production catalogs. Always verify your target before executing any change.

### Catalog and naming conventions

- Always use three-part naming: `catalog.schema.table`
- Development catalogs: `smartgrid_dev`, `smartgrid_staging`
- Production catalogs: `smartgrid_prod`
- Table prefixes: `bronze_*` (raw), `silver_*` (cleansed), `gold_*` (curated)
- Do not use `SELECT *` in production-bound code — always specify columns explicitly
- Currency: AUD. Energy measurements: kWh

### Default operating mode: non-production

- Default to `smartgrid_dev` unless the user explicitly confirms a production context
- If the catalog or schema is unspecified, ask before proceeding
- Do not infer production intent — require explicit confirmation

### Review requirements

- **Propose changes before executing** — never auto-run code that modifies data, schema, or configuration
- For any `DROP`, `TRUNCATE`, `DELETE`, or `INSERT OVERWRITE`: pause and require explicit confirmation
- For bulk operations: list all targets and get confirmation before proceeding
- Highlight any operation that cannot be easily reversed

### Destructive action warnings

Before proposing any of the following, state that the action is irreversible and ask for confirmation:

- `DROP TABLE`, `DROP SCHEMA`, `DROP CATALOG`
- `TRUNCATE TABLE`
- `DELETE FROM` without a restrictive `WHERE` clause
- `ALTER TABLE` that removes columns or changes column types
- `git push --force` or any force-push to a shared branch
- Deleting branches that may not have been merged

### Approved MCP connections

- **GitHub**: read and write access to connected repositories
- **Glean**: read-only knowledge lookup only
- All other MCP connections: **not approved** — ask before using

### Compute guidance

- Prefer the existing attached cluster or the default SQL warehouse
- Do not start a new cluster without user confirmation
- Flag compute-intensive operations before executing

### Regulatory context (energy sector)

Any code that aggregates or exports customer data should:

- Include a data classification comment
- Avoid PII in outputs or query results
- Not write raw customer data to public-facing catalogs

### Reminders

- You are operating with the user's own identity and permissions — no elevated access.
- Instructions guide behavior. They do not replace Unity Catalog permissions.
- If uncertain about intent, ask a clarifying question before proceeding.
