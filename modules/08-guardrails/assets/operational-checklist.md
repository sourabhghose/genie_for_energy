# Genie Code — Pre-Execution Operational Checklist

> Use this checklist before approving any Genie Code change in a sensitive environment.
> Takes approximately 2 minutes. Prevents the majority of avoidable mistakes.

---

## 1. Session scope

- [ ] I have stated the repo and branch explicitly at the start of this session
- [ ] The assistant has acknowledged the scope
- [ ] AGENTS.md (or CLAUDE.md) is present in this repo and reflects current operating rules
- [ ] I have confirmed which MCP connections are active for this session

---

## 2. Target verification

- [ ] The target catalog is confirmed: ___________________
- [ ] The target schema is confirmed: ___________________
- [ ] The target table(s) are confirmed: ___________________
- [ ] The target catalog is **NOT** a production catalog — OR — I have explicitly confirmed prod intent
- [ ] The branch I am working on is **NOT** main — OR — I have a specific reason and PR process in place

---

## 3. Change review

- [ ] I have read the **full diff** — not just the summary or description
- [ ] The change does exactly what I requested — nothing more, nothing less
- [ ] There are **no** `DROP`, `TRUNCATE`, or bulk `DELETE` statements I did not expect
- [ ] There are **no** schema-altering statements (`ALTER TABLE`, `DROP COLUMN`) I did not expect
- [ ] The change does not write to a table I cannot restore (no time-travel backup, no upstream restore path)
- [ ] Any downstream tables or views impacted by this change have been identified

---

## 4. Destructive action gate

*Complete this section only if the proposed change includes DROP, TRUNCATE, DELETE, or schema alteration.*

- [ ] I understand this action **cannot be easily reversed**
- [ ] I have confirmed the correct catalog (not prod, or explicitly approved for prod)
- [ ] I have confirmed the affected row / object count
- [ ] A backup or restore path exists (Delta time-travel, snapshot, etc.)
- [ ] This has been reviewed by at least one other person (for production changes)

---

## 5. Code quality spot-check

- [ ] No `SELECT *` in production-bound code
- [ ] All table references use three-part naming (`catalog.schema.table`)
- [ ] No hardcoded catalog or schema names that could break in a different environment
- [ ] No secrets, tokens, or connection strings in the code
- [ ] Data quality checks are present for silver-layer transformations

---

## 6. After execution

- [ ] The change produced the expected result
- [ ] No unexpected tables were modified (check Unity Catalog audit logs if needed)
- [ ] A commit or PR was created to document the change
- [ ] Usage is visible in `system.access.assistant_events`
- [ ] If this change affects a scheduled job or pipeline, it has been validated in dev before promoting

---

## Quick reference: when to use each checklist section

| Change type | Required sections |
|---|---|
| Read-only exploration | Section 1 only |
| Non-destructive code change | Sections 1, 2, 3, 5, 6 |
| Destructive data operation | All sections |
| Schema change | Sections 1, 2, 3, 4, 5, 6 |
| Branch / git operation | Section 1, plus confirm merge status |
| External tool action (MCP) | Section 1, plus confirm approved tool list |

---

## Post-session governance

After completing a Genie Code session involving data or schema changes:

```sql
-- Verify your session activity was logged
SELECT
  event_time,
  user_id,
  session_id,
  event_type,
  source_name
FROM system.access.assistant_events
WHERE user_id = current_user()
  AND event_time >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
ORDER BY event_time DESC;
```

---

*This checklist should be reviewed and updated quarterly, or when operating environment changes.*
