# Minimum Safe Setup — Genie Code for Enterprise

> This checklist covers the minimum configuration required before enabling Genie Code
> for a team in a sensitive or regulated environment.
> Complete all items before moving to production workloads.

---

## 1. Identity and access control

**Required:**

- [ ] All Genie Code users have been granted the **minimum required permissions** in Unity Catalog
  - Read access to approved catalogs only
  - No `DROP`, `TRUNCATE`, or `ALTER TABLE` on production catalogs unless explicitly required
  - No `CREATE CATALOG` or `CREATE SCHEMA` on prod — restrict to admins
- [ ] Production catalogs are named clearly and distinguishably (e.g., `*_prod`, `prod_*`)
- [ ] Non-production catalogs are provisioned for all Genie Code users (`*_dev`, `*_staging`)
- [ ] Unity Catalog data classification labels applied to tables containing PII or sensitive data
- [ ] Verify Genie Code is using **Agent Mode** (not DB-hosted legacy mode) — check Settings

---

## 2. Workspace instructions

**Required:**

- [ ] Workspace instructions have been configured by a workspace admin
- [ ] Instructions include:
  - [ ] Default catalog (non-prod)
  - [ ] Mandatory review step before destructive operations
  - [ ] Approved MCP server list
  - [ ] Data classification or handling rules relevant to the org
  - [ ] Prohibition on auto-pushing to main
- [ ] Instructions have been reviewed by at least one SME (security, data governance, or engineering lead)
- [ ] Instructions are documented in an internal runbook so they can be reproduced across workspaces

**If multiple workspaces:**

- [ ] Standardized instruction block applied to all workspaces where Genie Code is enabled
- [ ] Admin runbook documented for how to update instructions org-wide

---

## 3. Repository hygiene

**Required for every active repository:**

- [ ] `AGENTS.md` committed to repo root with:
  - [ ] Repo purpose statement
  - [ ] Branch rules (no direct push to main, use feature branches)
  - [ ] Catalog/schema rules (dev by default, prod requires confirmation)
  - [ ] Prohibited actions list
  - [ ] Code style conventions
- [ ] Branch protection rules enabled on `main`:
  - [ ] Require pull request before merging
  - [ ] Require at least one reviewer
  - [ ] Prohibit force-push
  - [ ] Prohibit deletion of main

**Optional but recommended:**

- [ ] `CLAUDE.md` (Claude Code-specific version) if the team uses Claude Code
- [ ] `.gitignore` rules for secrets and environment files

---

## 4. Compute and spend controls

**Required:**

- [ ] Budget alert set in **Account Console → Budgets**
  - Alert threshold: set to expected monthly compute budget
  - Alert recipient: team lead + Databricks admin
- [ ] Cluster policy in place for interactive clusters:
  - [ ] Maximum cluster size defined
  - [ ] **Auto-termination mandatory: < 1 hour** (FE workspace enforces this automatically; replicate in customer environments)
  - [ ] Single-node default unless workload requires multi-node
  - [ ] Restricted to approved node types
- [ ] Serverless compute spend limit reviewed (if serverless is enabled)

**If running in the shared FE workspace (e2-demo-field-eng):**

- [ ] Use shared clusters (US/EMEA/APJ) and `Shared Serverless` warehouse first
- [ ] Do not attach libraries to shared clusters — use user-level pip installs
- [ ] GPU clusters must be deleted after use — they are killed automatically daily
- [ ] All new catalogs tagged with `RemoveAfter = YYYY-MM-DD` immediately after creation

**Optional:**

- [ ] Separate budget alert for dev vs. prod workloads
- [ ] Cost dashboard based on system tables to track weekly compute by user

---

## 5. Usage monitoring

**Required:**

- [ ] Confirm `system.access.assistant_events` is accessible to your admin/governance team
- [ ] Create a basic query or dashboard to review weekly usage:

```sql
-- Weekly Genie Code usage summary
SELECT
  DATE_TRUNC('week', event_time) AS week,
  user_id,
  COUNT(*) AS interaction_count,
  COUNT(DISTINCT session_id) AS session_count
FROM system.access.assistant_events
WHERE event_time >= DATEADD(WEEK, -4, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
```

- [ ] Assign an owner to review usage weekly for the first 90 days
- [ ] Document the process for handling anomalous usage (unusual volume from a single user, unusual hours, etc.)

---

## 6. MCP governance

**Required:**

- [ ] Document which MCP integrations are **approved** for this workspace
- [ ] Communicate the approved list to all Genie Code users
- [ ] Include the approved list in workspace instructions
- [ ] Review per-user MCP configurations if any sensitive external connections are in scope

**Note:** Workspace-level MCP allowlists are not available today. Governance is currently per-user configuration + workspace instruction guidance.

---

## 7. User readiness

**Required before enabling for a team:**

- [ ] All users have completed the base Genie for Energy lab (or equivalent)
- [ ] All users understand the diff review process and have committed to reviewing before accepting
- [ ] All users have read the AGENTS.md for their active repositories
- [ ] Team has a shared understanding of: scope statements, safe prompt patterns, review habits
- [ ] An escalation path is documented: who to contact if a Genie Code session causes an unexpected change

---

## 8. Regulated industry additions

*Complete these additional items if you are in a HIPAA, PCI, financial services, or utility/energy regulatory context.*

- [ ] Confirm partner-powered AI features are enabled (required for Agent Mode + HIPAA compliance)
- [ ] Confirm your workspace is on AWS E2, Azure, or GCP (legacy PVC/single-tenant not supported)
- [ ] Cross-geo processing setting has been reviewed if operating in non-Americas regions
- [ ] Data handling policy reviewed: Genie Code sends table schemas and in-focus code context to the model provider. Confirm this is consistent with your data classification policy.
- [ ] Security questionnaire response reviewed and approved by your security team
- [ ] Internal legal/compliance review completed (if required by your org's AI usage policy)

---

## Sign-off

| Role | Name | Date | Sign-off |
|---|---|---|---|
| Workspace Admin | | | |
| Data Governance Lead | | | |
| Security/Compliance | | | |
| Team Lead | | | |

---

*This checklist should be reviewed when: Genie Code is first enabled, team membership changes significantly, new catalogs or workspaces are added, or MCP integrations change.*
