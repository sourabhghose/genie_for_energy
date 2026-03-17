---
name: job-deployer
description: "Deploys scheduled Lakeflow Jobs via Databricks SDK. Creates multi-task DAG jobs with cron schedules for energy ETL, pipelines, and reporting. Use when automating job deployment for energy/utilities workflows."
---

# Job Deployer

Deploy Databricks Lakeflow Jobs programmatically via the Databricks SDK. Creates multi-task DAG jobs with cron schedules for energy ETL, pipeline triggers, and reporting.

## When to Use

- Automating job deployment from config
- CI/CD for energy ETL or pipeline jobs
- Scheduling daily/hourly data refreshes
- Workshop demos requiring pre-configured jobs

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Job display name |
| `tasks` | Yes | List of task configs (notebook, SQL, pipeline, etc.) |
| `schedule` | No | Cron expression (e.g., `0 0 * * *` for daily) |
| `job_clusters` | No | Cluster config for tasks |
| `max_concurrent_runs` | No | Concurrency limit (default: 1) |

## Workflow

1. **Define tasks** — Notebook, SQL, pipeline, or Python tasks
2. **Set dependencies** — `depends_on` for DAG
3. **Configure schedule** — Cron or trigger
4. **Create** — `w.jobs.create()` or `w.jobs.reset()`

## Script Usage

```bash
python scripts/deploy_job.py \
  --name "Energy ETL Daily" \
  --config job_config.json
```

Or inline:

```bash
python scripts/deploy_job.py \
  --name "Energy ETL" \
  --schedule "0 6 * * *" \
  --pipeline-id <pipeline_id>
```

## Reference Files

- [references/job-config-patterns.md](references/job-config-patterns.md) — Common job configuration patterns

## Prerequisites

- Databricks SDK
- Notebooks/pipelines in workspace
- Job cluster or serverless (omit cluster for serverless)
