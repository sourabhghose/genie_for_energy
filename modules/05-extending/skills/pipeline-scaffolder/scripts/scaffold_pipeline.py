#!/usr/bin/env python3
"""
Scaffold medallion pipelines and create them via the Databricks Pipelines API.

Generates bronze/silver/gold SDP source files from SQL templates and creates the pipeline.
Target: main.sourabh_energy_workshop for energy/utilities data.

Usage:
    python scaffold_pipeline.py --name "Energy Medallion" --catalog main --schema sourabh_energy_workshop
"""

import argparse
import json
import sys
from pathlib import Path

from databricks.sdk import WorkspaceClient


def load_template(name: str, base_dir: Path) -> str:
    """Load SQL template from assets/."""
    p = base_dir / "assets" / f"{name}-template.sql"
    if not p.exists():
        raise FileNotFoundError(f"Template not found: {p}")
    return p.read_text()


def substitute(template: str, catalog: str, schema: str, source_path: str) -> str:
    """Replace placeholders in template."""
    return (
        template.replace("{{catalog}}", catalog)
        .replace("{{schema}}", schema)
        .replace("{{source_path}}", source_path)
    )


def build_pipeline_config(
    name: str,
    catalog: str,
    schema: str,
    source_path: str,
    templates_dir: Path,
) -> dict:
    """Build pipeline configuration for API."""
    bronze_sql = substitute(
        load_template("bronze", templates_dir),
        catalog, schema, source_path,
    )
    silver_sql = substitute(
        load_template("silver", templates_dir),
        catalog, schema, source_path,
    )
    gold_sql = substitute(
        load_template("gold", templates_dir),
        catalog, schema, source_path,
    )

    return {
        "name": name,
        "storage": f"{catalog}.{schema}.pipeline_storage",
        "target": f"{catalog}.{schema}",
        "configuration": {
            "catalog": catalog,
            "schema": schema,
            "source_path": source_path,
        },
        "libraries": [
            {"notebook": {"path": ""}},
        ],
        "clusters": [
            {
                "label": "default",
                "num_workers": 0,
                "custom_tags": {"cluster_type": "serverless"},
            }
        ],
        "source": [
            {"name": "bronze", "path": "bronze.sql", "language": "SQL", "content": bronze_sql},
            {"name": "silver", "path": "silver.sql", "language": "SQL", "content": silver_sql},
            {"name": "gold", "path": "gold.sql", "language": "SQL", "content": gold_sql},
        ],
    }


def create_pipeline_via_api(w: WorkspaceClient, config: dict, notebook_path: str) -> dict:
    """Create pipeline using Pipelines API. Requires notebook at notebook_path."""
    body = {
        "name": config["name"],
        "storage": config["storage"],
        "target": config["target"],
        "configuration": config.get("configuration", {}),
        "clusters": config.get("clusters", []),
        "libraries": [{"notebook": {"path": notebook_path}}],
    }

    resp = w.api_client.do("POST", "/api/2.0/pipelines", body=body)

    if resp.get("pipeline_id"):
        return {
            "pipeline_id": resp["pipeline_id"],
            "name": resp.get("name", config["name"]),
            "state": resp.get("state", "UNKNOWN"),
        }
    raise RuntimeError(f"Create failed: {resp}")


def scaffold_and_create(
    name: str,
    catalog: str,
    schema: str,
    source_path: str | None = None,
    output_dir: str | None = None,
    create: bool = True,
    notebook_path: str | None = None,
) -> dict:
    """
    Scaffold pipeline files and optionally create the pipeline.

    For create=True, provide notebook_path (workspace path to SDP notebook)
    or use output_dir and upload files, then create pipeline manually.

    Returns:
        dict with pipeline_id (if create=True), source_files, config
    """
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent

    default_source = f"/Volumes/{catalog}/{schema}/raw/"
    src = source_path or default_source

    config = build_pipeline_config(name, catalog, schema, src, templates_dir)

    out_dir = Path(output_dir) if output_dir else Path.cwd() / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    for src_item in config["source"]:
        (out_dir / src_item["path"]).write_text(src_item["content"])
    (out_dir / "pipeline_config.json").write_text(json.dumps(config, indent=2))

    result = {
        "config": config,
        "source_files": [s["path"] for s in config["source"]],
        "output_dir": str(out_dir),
    }

    if create and notebook_path:
        w = WorkspaceClient()
        created = create_pipeline_via_api(w, config, notebook_path)
        result["pipeline_id"] = created["pipeline_id"]
        result["name"] = created["name"]
        result["state"] = created["state"]

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold and create medallion pipeline")
    parser.add_argument("--name", required=True, help="Pipeline name")
    parser.add_argument("--catalog", required=True, help="Unity Catalog name")
    parser.add_argument("--schema", required=True, help="Schema name")
    parser.add_argument("--source-path", help="Volume path for raw data")
    parser.add_argument("--output-dir", help="Directory to write source files")
    parser.add_argument("--notebook-path", help="Workspace path to SDP notebook (required for --create)")
    parser.add_argument("--no-create", action="store_true", help="Only scaffold, do not create pipeline")
    args = parser.parse_args()

    try:
        result = scaffold_and_create(
            name=args.name,
            catalog=args.catalog,
            schema=args.schema,
            source_path=args.source_path,
            output_dir=args.output_dir,
            create=not args.no_create,
            notebook_path=args.notebook_path,
        )
        print("Pipeline scaffolded:")
        print(f"  output_dir: {result['output_dir']}")
        print(f"  source_files: {result['source_files']}")
        if "pipeline_id" in result:
            print(f"  pipeline_id: {result['pipeline_id']}")
            print(f"  name: {result['name']}")
        elif not args.no_create and not args.notebook_path:
            print("  (Use --notebook-path to create pipeline via API)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
