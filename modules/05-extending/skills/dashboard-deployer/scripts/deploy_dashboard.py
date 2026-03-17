#!/usr/bin/env python3
"""
Deploy AI/BI (Lakeview) dashboards from JSON templates via Databricks SDK.

Creates and optionally publishes dashboards for energy ops and sustainability use cases.
Tables reference main.sourabh_energy_workshop schema.

Usage:
    python deploy_dashboard.py --template assets/ops-center-template.json --display-name "Ops Center" --warehouse-id <id>
"""

import argparse
import json
import sys
from pathlib import Path

from databricks.sdk import WorkspaceClient


def load_template(path: str) -> dict:
    """Load dashboard JSON template."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    with open(p, "r") as f:
        return json.load(f)


def create_dashboard(
    w: WorkspaceClient,
    template: dict,
    display_name: str,
    warehouse_id: str,
    parent_path: str = "/Workspace/Users/me/Dashboards",
) -> dict:
    """Create dashboard via workspace API."""
    body = {
        "display_name": display_name,
        "serialized_dashboard": json.dumps(template),
        "warehouse_id": warehouse_id,
        "parent_path": parent_path,
    }
    resp = w.api_client.do("POST", "/api/2.0/workspace/dashboards", body=body)
    return resp


def publish_dashboard(w: WorkspaceClient, dashboard_id: str, warehouse_id: str | None = None) -> None:
    """Publish dashboard for sharing."""
    body = {"embed_credentials": True}
    if warehouse_id:
        body["warehouse_id"] = warehouse_id
    w.api_client.do(
        "POST",
        f"/api/2.0/lakeview/dashboards/{dashboard_id}/published",
        body=body,
    )


def deploy(
    template_path: str,
    display_name: str,
    warehouse_id: str,
    parent_path: str | None = None,
    publish: bool = True,
) -> dict:
    """
    Deploy a dashboard from a template.

    Returns:
        dict with dashboard_id, path, display_name
    """
    w = WorkspaceClient()
    template = load_template(template_path)
    parent = parent_path or "/Workspace/Users/me/Dashboards"

    resp = create_dashboard(
        w, template, display_name, warehouse_id, parent
    )

    dashboard_id = resp.get("dashboard_id")
    if not dashboard_id:
        raise RuntimeError(f"Create failed: {resp}")

    if publish:
        try:
            publish_dashboard(w, dashboard_id, warehouse_id)
        except Exception as e:
            print(f"Warning: Publish failed: {e}", file=sys.stderr)

    return {
        "dashboard_id": dashboard_id,
        "path": resp.get("path", ""),
        "display_name": resp.get("display_name", display_name),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy AI/BI dashboard from template")
    parser.add_argument("--template", required=True, help="Path to JSON template")
    parser.add_argument("--display-name", required=True, help="Dashboard display name")
    parser.add_argument("--warehouse-id", required=True, help="SQL warehouse ID")
    parser.add_argument("--parent-path", help="Workspace folder path")
    parser.add_argument("--publish", action="store_true", default=True, help="Publish after create")
    parser.add_argument("--no-publish", action="store_true", dest="no_publish", help="Do not publish")
    args = parser.parse_args()

    do_publish = args.publish and not args.no_publish

    try:
        result = deploy(
            template_path=args.template,
            display_name=args.display_name,
            warehouse_id=args.warehouse_id,
            parent_path=args.parent_path,
            publish=do_publish,
        )
        print("Deployed dashboard:")
        print(f"  dashboard_id: {result['dashboard_id']}")
        print(f"  path: {result['path']}")
        print(f"  display_name: {result['display_name']}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
