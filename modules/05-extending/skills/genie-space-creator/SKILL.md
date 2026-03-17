---
name: genie-space-creator
description: "Creates Genie Spaces programmatically via Databricks SDK. Inspects gold tables, generates sample questions, and calls the Genie API to create spaces for natural language SQL exploration. Use when automating Genie Space creation for energy/utilities data or building CI/CD for Genie deployments."
---

# Genie Space Creator

Create Genie Spaces programmatically using the Databricks SDK. Inspects gold tables in `main.sourabh_energy_workshop`, generates sample questions, and deploys spaces via the Genie API.

## When to Use

- Automating Genie Space creation from gold tables
- CI/CD pipelines for Genie deployments
- Bulk creation of spaces for multiple schemas or regions
- Energy workshop demos requiring pre-configured spaces

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `catalog` | Yes | Unity Catalog name (e.g., `main`) |
| `schema` | Yes | Schema with gold tables (e.g., `sourabh_energy_workshop`) |
| `warehouse_id` | Yes | SQL warehouse ID for query execution |
| `title` | No | Space display title (default: schema-based) |
| `parent_path` | No | Workspace folder path (e.g., `/Workspace/Users/me/Genie`) |

## Workflow

1. **Inspect gold tables** — List tables in the schema
2. **Generate sample questions** — From table/column names and energy domain
3. **Build serialized space** — Tables + sample questions + instructions
4. **Call POST /api/genie/create_space** — Create the space

## Script Usage

```bash
python scripts/create_genie_space.py \
  --catalog main \
  --schema sourabh_energy_workshop \
  --warehouse-id <warehouse_id> \
  --title "Energy Analytics Genie"
```

## Example Output

```
Created Genie Space:
  space_id: abc123...
  title: Energy Analytics Genie
  Tables: main.sourabh_energy_workshop.gold_daily_consumption, ...
  Sample questions: 5
```

## Reference Files

- [references/serialized-space-schema.md](references/serialized-space-schema.md) — API payload structure

## Prerequisites

- Databricks SDK: `pip install databricks-sdk`
- Authenticated workspace (profile or env vars)
- Gold tables in Unity Catalog
- SQL warehouse (Serverless recommended)
