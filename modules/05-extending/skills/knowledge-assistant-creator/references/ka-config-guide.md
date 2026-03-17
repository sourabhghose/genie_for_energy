# Knowledge Assistant Configuration Guide

## Overview

Knowledge Assistants (KAs) are RAG chatbots that answer questions over indexed documents. Documents are stored in Unity Catalog volumes.

## API Endpoints (KnowledgeAssistants.v1)

| Action | Method | Endpoint |
|--------|--------|----------|
| Create KA | POST | `/api/2.0/knowledge-assistants` |
| Get KA | GET | `/api/2.0/knowledge-assistants/{id}` |
| Update KA | PATCH | `/api/2.0/knowledge-assistants/{id}` |
| Delete KA | DELETE | `/api/2.0/knowledge-assistants/{id}` |
| Create Knowledge Source | POST | `/api/2.0/knowledge-assistants/{id}/knowledge-sources` |
| Sync Sources | POST | `/api/2.0/knowledge-assistants/{id}/sync` |

**Note:** Exact API paths may vary. Check [Databricks Knowledge Assistants API](https://docs.databricks.com/api/workspace/knowledgeassistants) for current structure.

## Create Request Body

```json
{
  "name": "Energy Policy Assistant",
  "description": "Answers questions about energy policies and regulatory documents",
  "instructions": "You are an energy expert. Cite sources. Be concise."
}
```

## Knowledge Source Types

### Volume (files)

```json
{
  "type": "volume",
  "path": "/Volumes/main/sourabh_energy_workshop/policies/"
}
```

### Vector Search Index

```json
{
  "type": "vector_search",
  "index_name": "catalog.schema.index_name"
}
```

## Supported Document Formats

- PDF
- TXT
- MD (Markdown)
- DOC/DOCX
- PPT/PPTX

## Volume Path Format

```
/Volumes/<catalog>/<schema>/<volume_name>/[subpath/]
```

Example: `/Volumes/main/sourabh_energy_workshop/regulatory_filings/2025/`

## Endpoint Status

| Status | Meaning |
|--------|---------|
| PROVISIONING | Being created (2-5 minutes) |
| ONLINE | Ready to use |
| OFFLINE | Not running |

## Example: Create via Python

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Create KA
resp = w.api_client.do(
    "POST",
    "/api/2.0/knowledge-assistants",
    body={
        "name": "Energy Policy Assistant",
        "description": "RAG over energy policies",
        "instructions": "Cite sources. Be concise.",
    },
)
tile_id = resp["id"]

# Add volume source
w.api_client.do(
    "POST",
    f"/api/2.0/knowledge-assistants/{tile_id}/knowledge-sources",
    body={"type": "volume", "path": "/Volumes/main/sourabh_energy_workshop/policies/"},
)

# Sync
w.api_client.do("POST", f"/api/2.0/knowledge-assistants/{tile_id}/sync", body={})
```

## Prerequisites

- Unity Catalog enabled
- Serverless compute
- Production MLflow monitoring
- Foundation model access (system.ai)
- Serverless budget policy with nonzero budget
