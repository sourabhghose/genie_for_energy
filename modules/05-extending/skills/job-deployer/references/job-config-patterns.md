# Job Configuration Patterns

## Pipeline Task (Energy ETL)

```json
{
  "name": "Energy ETL Daily",
  "schedule": "0 6 * * *",
  "timezone": "America/New_York",
  "tasks": [
    {
      "task_key": "run_energy_pipeline",
      "pipeline_task": {
        "pipeline_id": "your-pipeline-id"
      }
    }
  ]
}
```

## Multi-Task DAG (Bronze → Silver → Gold)

```json
{
  "name": "Energy Medallion ETL",
  "schedule": "0 5 * * *",
  "tasks": [
    {
      "task_key": "bronze",
      "notebook_task": {
        "notebook_path": "/Workspace/Users/me/energy_etl/bronze_ingest",
        "source": "WORKSPACE"
      }
    },
    {
      "task_key": "silver",
      "depends_on": ["bronze"],
      "notebook_task": {
        "notebook_path": "/Workspace/Users/me/energy_etl/silver_transform",
        "source": "WORKSPACE"
      }
    },
    {
      "task_key": "gold",
      "depends_on": ["silver"],
      "notebook_task": {
        "notebook_path": "/Workspace/Users/me/energy_etl/gold_aggregate",
        "source": "WORKSPACE"
      }
    }
  ]
}
```

## SQL Task (Reporting)

```json
{
  "name": "Energy Daily Report",
  "schedule": "0 8 * * *",
  "tasks": [
    {
      "task_key": "refresh_mv",
      "sql_task": {
        "query": "REFRESH MATERIALIZED VIEW main.sourabh_energy_workshop.daily_summary",
        "warehouse_id": "your-warehouse-id"
      }
    }
  ]
}
```

## Pipeline + Notification

```json
{
  "name": "Energy Pipeline with Alerts",
  "schedule": "0 6 * * *",
  "tasks": [
    {
      "task_key": "run_pipeline",
      "pipeline_task": {
        "pipeline_id": "energy-sdp-pipeline-id"
      }
    }
  ],
  "email_notifications": {
    "on_failure": ["ops@example.com"],
    "on_success": []
  }
}
```

## Cron Expressions

| Expression | Meaning |
|------------|---------|
| `0 6 * * *` | Daily at 6:00 AM UTC |
| `0 */2 * * *` | Every 2 hours |
| `0 0 * * 1` | Weekly on Monday at midnight |
| `0 5 1 * *` | Monthly on 1st at 5:00 AM |

## Serverless vs Job Clusters

**Serverless** (default for notebook/Python): Omit `job_clusters` and `new_cluster` from tasks.

**Job clusters** (for custom Spark config):

```json
{
  "job_clusters": [
    {
      "job_cluster_key": "shared",
      "new_cluster": {
        "spark_version": "15.4.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 2
      }
    }
  ],
  "tasks": [
    {
      "task_key": "my_task",
      "job_cluster_key": "shared",
      "notebook_task": { ... }
    }
  ]
}
```
