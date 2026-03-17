#!/usr/bin/env python3
"""
Deploy Databricks Lakeflow Jobs via the Databricks SDK.

Creates multi-task DAG jobs with cron schedules for energy ETL and pipeline triggers.
Supports notebook, SQL, and pipeline tasks.

Usage:
    python deploy_job.py --name "Energy ETL Daily" --config job_config.json
    python deploy_job.py --name "Energy ETL" --schedule "0 6 * * *" --pipeline-id <id>
"""

import argparse
import json
import sys
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import (
    JobSettings,
    Task,
    NotebookTask,
    PipelineTask,
    SqlTask,
    Schedule,
    CronSchedule,
)


def load_config(path: str) -> dict:
    """Load job config from JSON file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with open(p, "r") as f:
        return json.load(f)


def build_tasks(config: dict) -> list[Task]:
    """Build task list from config."""
    tasks = []
    for t in config.get("tasks", []):
        task_key = t["task_key"]
        depends_on = [{"task_key": d} for d in t.get("depends_on", [])]

        if "notebook_task" in t:
            nt = t["notebook_task"]
            task = Task(
                task_key=task_key,
                depends_on=depends_on if depends_on else None,
                notebook_task=NotebookTask(
                    notebook_path=nt["notebook_path"],
                    source=nt.get("source", "WORKSPACE"),
                ),
            )
        elif "pipeline_task" in t:
            pt = t["pipeline_task"]
            task = Task(
                task_key=task_key,
                depends_on=depends_on if depends_on else None,
                pipeline_task=PipelineTask(pipeline_id=pt["pipeline_id"]),
            )
        elif "sql_task" in t:
            st = t["sql_task"]
            task = Task(
                task_key=task_key,
                depends_on=depends_on if depends_on else None,
                sql_task=SqlTask(
                    query=st.get("query"),
                    warehouse_id=st.get("warehouse_id"),
                    file=st.get("file"),
                ),
            )
        else:
            raise ValueError(f"Unknown task type for {task_key}")

        tasks.append(task)
    return tasks


def create_schedule(cron: str, timezone: str = "UTC") -> Schedule:
    """Build cron schedule."""
    return Schedule(
        cron_schedule=CronSchedule(
            quartz_cron_expression=cron,
            timezone_id=timezone,
        ),
        pause_status="UNPAUSED",
    )


def _job_create_kwargs(settings: JobSettings) -> dict:
    """Convert JobSettings to kwargs for w.jobs.create."""
    out = {"name": settings.name, "tasks": settings.tasks}
    if settings.max_concurrent_runs is not None:
        out["max_concurrent_runs"] = settings.max_concurrent_runs
    if settings.schedule is not None:
        out["schedule"] = settings.schedule
    return out


def deploy_job(
    name: str,
    config_path: str | None = None,
    schedule: str | None = None,
    pipeline_id: str | None = None,
    notebook_path: str | None = None,
    warehouse_id: str | None = None,
    max_concurrent_runs: int = 1,
) -> dict:
    """
    Deploy a job. Uses config file or inline params.

    Returns:
        dict with job_id, run_url
    """
    w = WorkspaceClient()

    if config_path:
        config = load_config(config_path)
        tasks = build_tasks(config)
        job_name = config.get("name", name)
    else:
        tasks = []
        if pipeline_id:
            tasks.append(
                Task(
                    task_key="run_pipeline",
                    pipeline_task=PipelineTask(pipeline_id=pipeline_id),
                )
            )
        elif notebook_path:
            tasks.append(
                Task(
                    task_key="run_notebook",
                    notebook_task=NotebookTask(
                        notebook_path=notebook_path,
                        source="WORKSPACE",
                    ),
                )
            )
        else:
            raise ValueError("Provide config_path, pipeline_id, or notebook_path")
        job_name = name

    settings = JobSettings(
        name=job_name,
        tasks=tasks,
        max_concurrent_runs=max_concurrent_runs,
    )

    if schedule:
        settings.schedule = create_schedule(schedule)

    job = w.jobs.create(**_job_create_kwargs(settings))

    return {
        "job_id": job.job_id,
        "name": job_name,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy Lakeflow Job")
    parser.add_argument("--name", required=True, help="Job name")
    parser.add_argument("--config", help="Path to job config JSON")
    parser.add_argument("--schedule", help="Cron expression (e.g., 0 6 * * * for 6am daily)")
    parser.add_argument("--pipeline-id", help="Pipeline ID for pipeline task")
    parser.add_argument("--notebook-path", help="Notebook path for notebook task")
    parser.add_argument("--warehouse-id", help="Warehouse ID for SQL tasks")
    parser.add_argument("--max-concurrent-runs", type=int, default=1)
    args = parser.parse_args()

    try:
        result = deploy_job(
            name=args.name,
            config_path=args.config,
            schedule=args.schedule,
            pipeline_id=args.pipeline_id,
            notebook_path=args.notebook_path,
            warehouse_id=args.warehouse_id,
            max_concurrent_runs=args.max_concurrent_runs,
        )
        print("Deployed job:")
        print(f"  job_id: {result['job_id']}")
        print(f"  name: {result['name']}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
