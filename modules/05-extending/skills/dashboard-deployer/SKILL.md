---
name: dashboard-deployer
description: "Deploys AI/BI (Lakeview) dashboards programmatically via Databricks SDK. Creates and publishes dashboards from JSON templates for energy ops centers and sustainability metrics. Use when automating dashboard deployment for energy/utilities use cases."
---

# Dashboard Deployer

Deploy Databricks AI/BI (Lakeview) dashboards programmatically via the Databricks SDK. Uses JSON templates for energy operations and sustainability dashboards.

## When to Use

- Automating dashboard deployment from templates
- CI/CD for energy ops or sustainability dashboards
- Deploying multiple dashboards for different regions
- Workshop demos requiring pre-built dashboards

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `template_path` | Yes | Path to JSON template (e.g., `assets/ops-center-template.json`) |
| `display_name` | Yes | Dashboard display name |
| `warehouse_id` | Yes | SQL warehouse ID |
| `parent_path` | No | Workspace folder (default: `/Workspace/Users/me/Dashboards`) |
| `publish` | No | Publish after create (default: true) |

## Workflow

1. **Load template** — Read JSON from `assets/` or custom path
2. **Validate** — Ensure datasets reference `main.sourabh_energy_workshop` tables
3. **Create** — POST /api/2.0/workspace/dashboards
4. **Publish** — Optional publish for sharing

## Script Usage

```bash
python scripts/deploy_dashboard.py \
  --template assets/ops-center-template.json \
  --display-name "Energy Ops Center" \
  --warehouse-id <warehouse_id> \
  --publish
```

## Templates

| Template | Use Case |
|----------|----------|
| `assets/ops-center-template.json` | Operations center: KPIs, alerts, regional trends |
| `assets/sustainability-template.json` | Sustainability: carbon, renewables, efficiency |

## Reference

- [databricks-aibi-dashboards](../databricks-aibi-dashboards/SKILL.md) — Full validation and widget specs
- **CRITICAL**: Test all SQL queries via `execute_sql` before deploying

## Prerequisites

- Databricks SDK
- Tables in `main.sourabh_energy_workshop` schema
- SQL warehouse (Serverless recommended)
