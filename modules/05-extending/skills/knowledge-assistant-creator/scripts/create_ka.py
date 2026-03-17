#!/usr/bin/env python3
"""
Create a Knowledge Assistant (RAG chatbot) via the Databricks Knowledge Assistants API.

Indexes documents from a Unity Catalog volume for energy policies, regulatory docs, and FAQs.
Uses KnowledgeAssistants.v1 API.

Usage:
    python create_ka.py --name "Energy Policy Assistant" --volume-path /Volumes/main/sourabh_energy_workshop/policies/
"""

import argparse
import sys

from databricks.sdk import WorkspaceClient


def create_knowledge_assistant(
    name: str,
    volume_path: str,
    description: str | None = None,
    instructions: str | None = None,
) -> dict:
    """
    Create a Knowledge Assistant with a volume-based knowledge source.

    Returns:
        dict with tile_id, name, endpoint_status
    """
    w = WorkspaceClient()

    desc = description or f"RAG assistant over documents in {volume_path}"
    instr = instructions or (
        "You are an energy and utilities expert. Answer questions based on the indexed documents. "
        "Cite sources when possible. Be concise and accurate."
    )

    # Create Knowledge Assistant (KnowledgeAssistants.v1 API)
    body = {
        "name": name,
        "description": desc,
        "instructions": instr,
    }

    try:
        resp = w.api_client.do(
            "POST",
            "/api/2.0/knowledge-assistants",
            body=body,
        )
    except Exception as e:
        # Fallback: try alternate API path if Knowledge Assistants use different endpoint
        if "404" in str(e) or "not found" in str(e).lower():
            raise RuntimeError(
                "Knowledge Assistants API may require a different endpoint. "
                "Check Databricks docs for KnowledgeAssistants.v1 API. "
                f"Original error: {e}"
            ) from e
        raise

    tile_id = resp.get("id") or resp.get("tile_id") or resp.get("knowledge_assistant_id")
    if not tile_id:
        raise RuntimeError(f"Create succeeded but no ID returned: {resp}")

    # Add knowledge source (volume path)
    try:
        w.api_client.do(
            "POST",
            f"/api/2.0/knowledge-assistants/{tile_id}/knowledge-sources",
            body={
                "type": "volume",
                "path": volume_path.rstrip("/"),
            },
        )
    except Exception as e:
        print(f"Warning: Could not add knowledge source: {e}", file=sys.stderr)
        print("  Add the volume path manually in the Databricks UI.", file=sys.stderr)

    # Sync knowledge sources
    try:
        w.api_client.do(
            "POST",
            f"/api/2.0/knowledge-assistants/{tile_id}/sync",
            body={},
        )
    except Exception as e:
        print(f"Warning: Could not trigger sync: {e}", file=sys.stderr)

    return {
        "tile_id": tile_id,
        "name": resp.get("name", name),
        "description": resp.get("description", desc),
        "endpoint_status": resp.get("endpoint_status", "PROVISIONING"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Knowledge Assistant")
    parser.add_argument("--name", required=True, help="KA display name")
    parser.add_argument("--volume-path", required=True, help="Volume path (e.g., /Volumes/main/schema/docs/)")
    parser.add_argument("--description", help="KA description")
    parser.add_argument("--instructions", help="System instructions for the KA")
    args = parser.parse_args()

    try:
        result = create_knowledge_assistant(
            name=args.name,
            volume_path=args.volume_path,
            description=args.description,
            instructions=args.instructions,
        )
        print("Created Knowledge Assistant:")
        print(f"  tile_id: {result['tile_id']}")
        print(f"  name: {result['name']}")
        print(f"  endpoint_status: {result['endpoint_status']}")
        print("  (Provisioning may take 2-5 minutes)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
