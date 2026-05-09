# Safe Prompt Patterns — Genie Code

> Reference guide for participants and facilitators.
> Copy these patterns and adapt them to your own workflows.

---

## The anatomy of a safe prompt

A safe Genie Code prompt has four components:

```
[SCOPE]      — which repo, branch, catalog
[TASK]       — what you want to achieve
[CONSTRAINTS] — what not to do, what to confirm first
[REVIEW GATE] — explicit "don't execute yet" instruction
```

---

## Safe prompt templates

### 1. Safe exploration (read-only)

```
Context: genie_for_energy repo, main branch, smartgrid_dev catalog.

Without writing or executing any code, explain:
- What does the silver_meter_readings table contain?
- Where does it get its data from?
- What downstream tables depend on it?

I want to understand the lineage before making any changes.
```

---

### 2. Safe change proposal

```
Context: genie_for_energy repo, feature/quality-checks branch, smartgrid_dev catalog only.

I want to add a data quality check to the silver_meter_readings pipeline 
that flags records where consumption_kwh is negative or null.

Before making any changes:
1. Show me the current transformation logic
2. Propose the addition as a diff — do not execute
3. Confirm which catalog and table will be affected
4. Identify any downstream tables that might be impacted

I will review and approve before you run anything.
```

---

### 3. Safe bulk operation

```
Context: genie_for_energy repo, feature/rename-columns branch, smartgrid_dev only.

I want to rename the column `kwh_consumed` to `consumption_kwh` 
across the silver layer tables to match our naming standard.

Before proposing any changes:
1. List every table in the silver schema that contains this column
2. List every downstream gold table or view that references it
3. Show me the full list of affected objects and ask me to confirm scope
4. Then propose the changes one table at a time — not all at once

Do not execute anything until I confirm each change.
```

---

### 4. Safe destructive operation (with staged approach)

```
Context: smartgrid_dev catalog only.

I want to remove old test data from the bronze_meter_readings_test table 
(rows from before 2024-01-01). This is dev data only, not production.

Before proceeding:
1. Show me how many rows would be affected by this delete
2. Confirm the table is in smartgrid_dev, not smartgrid_prod
3. Propose the DELETE statement with a clear WHERE clause — do not run yet
4. Ask me to confirm before executing

Do not use TRUNCATE. Use a targeted DELETE with a date filter.
```

---

### 5. Safe debugging session

```
Context: genie_for_energy repo, feature/pipeline-fix branch.

The silver_meter_readings pipeline is failing with the following error:
[paste error message here]

Please:
1. Diagnose the cause by reading the existing code (do not modify yet)
2. Propose a fix as a diff
3. Explain what the fix does and why
4. Do not execute — I will review and run it myself

If the fix requires changes to more than one file, list all files first.
```

---

### 6. Safe session opener (scope statement)

```
For this session:
- Repository: genie_for_energy
- Branch: feature/[your-branch]
- Catalog: smartgrid_dev only
- Scope: [notebook name or specific task]

Do not read from or modify any other repository, branch, or catalog.
If I ask you to do something outside this scope, remind me and ask for confirmation.
```

---

## Risky prompt patterns — and why to avoid them

---

### Risky: no scope

```
# RISKY — no repo, branch, or catalog specified
Fix the pipeline.
```

**Why risky:** The assistant doesn't know which pipeline, which branch, or which catalog. It may make assumptions that lead to changes in the wrong place.

**Fix:** Always open with a scope statement (template 6 above).

---

### Risky: "just do it"

```
# RISKY — no review gate
Update all the notebooks to use the new catalog naming convention 
and push to main.
```

**Why risky:**
- No scope — "all notebooks" is unbounded
- "Push to main" skips PR review
- No diff review step
- Could affect files across the entire repo

**Safe version:**
```
I'm on branch feature/rename-catalog in genie_for_energy.
I want to update notebooks to use smartgrid_dev instead of the old dev_energy catalog name.

First: list every notebook that references dev_energy.
Then: propose the change in one notebook at a time — do not execute yet.
After I approve each change, I will create a PR to main myself.
Do not push to main directly.
```

---

### Risky: destructive without scope

```
# RISKY — no catalog confirmation, no row-count check
Delete all the test records from the meter readings table.
```

**Why risky:** Which catalog? Which table? How many rows? Is there a backup? "Test records" is ambiguous.

**Safe version:**
```
In smartgrid_dev (not prod), I want to delete rows from bronze_meter_readings 
where the source_flag = 'TEST'. 

Before doing anything:
1. How many rows would this affect?
2. Confirm we're in smartgrid_dev
3. Show me the DELETE statement — don't run it yet
```

---

### Risky: sends to external system without confirmation

```
# RISKY — triggers external action immediately
Tell the team on Slack that the pipeline is fixed.
```

**Why risky:** Premature announcement; wrong channel risk; external action without user review.

**Safe version:**
```
Draft a Slack message to #data-engineering saying the silver_meter_readings 
pipeline issue has been resolved. Show me the draft — do not send yet. 
I'll review the message and send it manually.
```

---

## Quick reference card

| Situation | Safe pattern |
|---|---|
| Starting any session | Use scope statement template first |
| Exploring before changing | "Without executing any code, describe..." |
| Proposing a change | "Show me the diff — do not run yet" |
| Bulk operations | "List all affected objects first" |
| Destructive operations | "Show row count, confirm catalog, then propose" |
| External tool actions | "Show me the draft — I'll take the action myself" |
| Rollbacks | "Propose git revert, not git reset or force-push" |
