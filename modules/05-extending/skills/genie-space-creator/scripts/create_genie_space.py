#!/usr/bin/env python3
"""
Create a Genie Space programmatically from gold tables in a Unity Catalog schema.

Inspects tables, generates sample questions for energy/utilities use cases,
and calls the Databricks Genie API to create the space.

Usage:
    python create_genie_space.py --catalog main --schema sourabh_energy_workshop --warehouse-id <id>
"""

import argparse
import json
import sys
from databricks.sdk import WorkspaceClient


def get_gold_tables(w: WorkspaceClient, catalog: str, schema: str) -> list[str]:
    """List tables in the schema (gold layer)."""
    try:
        tables = list(w.tables.list(catalog_name=catalog, schema_name=schema))
        return [f"{catalog}.{schema}.{t.name}" for t in tables if t.name]
    except Exception as e:
        print(f"Error listing tables: {e}", file=sys.stderr)
        return []


def generate_sample_questions(tables: list[str], schema: str) -> list[str]:
    """Generate sample questions for energy/utilities domain."""
    base = [
        f"What is the total consumption by region in {schema}?",
        "Which region has the highest average usage?",
        "Show me daily consumption trends for the last 30 days.",
        "How many customers are in each region?",
        "What are the top 5 meters by consumption?",
    ]
    if tables:
        base.append(f"Summarize data from {tables[0]}.")
    return base[:6]


def build_serialized_space(
    table_identifiers: list[str],
    sample_questions: list[str],
    description: str,
) -> str:
    """Build the serialized space payload for the Genie API."""
    payload = {
        "layout": {"type": "GRID"},
        "components": [],
        "tableIdentifiers": table_identifiers,
        "sampleQuestions": sample_questions,
        "instructions": (
            "You are exploring energy and utilities data. "
            "Use tables from main.sourabh_energy_workshop. "
            "Regions: Northeast, Southeast, Midwest, Southwest, Northwest. "
            "Answer in clear, concise language."
        ),
    }
    return json.dumps(payload)


def create_genie_space(
    catalog: str,
    schema: str,
    warehouse_id: str,
    title: str | None = None,
    parent_path: str | None = None,
    description: str | None = None,
) -> dict:
    """
    Create a Genie Space via the Databricks API.

    Returns:
        dict with space_id, title, description, created_at
    """
    w = WorkspaceClient()

    tables = get_gold_tables(w, catalog, schema)
    if not tables:
        raise ValueError(f"No tables found in {catalog}.{schema}")

    sample_questions = generate_sample_questions(tables, schema)
    desc = description or f"Natural language SQL exploration for {catalog}.{schema}"
    display_title = title or f"{schema} Analytics"

    serialized = build_serialized_space(tables, sample_questions, desc)

    body = {
        "warehouse_id": warehouse_id,
        "serialized_space": serialized,
        "title": display_title,
        "description": desc,
    }
    if parent_path:
        body["parent_path"] = parent_path

    resp = w.api_client.do("POST", "/api/genie/create_space", body=body)

    if resp.get("space_id"):
        return {
            "space_id": resp["space_id"],
            "title": resp.get("title", display_title),
            "description": resp.get("description", desc),
            "created_at": resp.get("created_at", ""),
            "tables": tables,
            "sample_questions": sample_questions,
        }
    raise RuntimeError(f"Create failed: {resp}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Genie Space from gold tables")
    parser.add_argument("--catalog", required=True, help="Unity Catalog name")
    parser.add_argument("--schema", required=True, help="Schema name")
    parser.add_argument("--warehouse-id", required=True, help="SQL warehouse ID")
    parser.add_argument("--title", help="Space display title")
    parser.add_argument("--parent-path", help="Workspace folder path")
    parser.add_argument("--description", help="Space description")
    args = parser.parse_args()

    try:
        result = create_genie_space(
            catalog=args.catalog,
            schema=args.schema,
            warehouse_id=args.warehouse_id,
            title=args.title,
            parent_path=args.parent_path,
            description=args.description,
        )
        print("Created Genie Space:")
        print(f"  space_id: {result['space_id']}")
        print(f"  title: {result['title']}")
        print(f"  tables: {len(result['tables'])}")
        print(f"  sample_questions: {len(result['sample_questions'])}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
