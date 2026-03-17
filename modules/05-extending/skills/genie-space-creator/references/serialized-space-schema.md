# Genie Space API Payload Structure

## POST /api/genie/create_space

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `warehouse_id` | string | Yes | SQL warehouse ID for query execution |
| `serialized_space` | string | Yes | JSON string of the space configuration |
| `title` | string | No | Display title override |
| `description` | string | No | Space description |
| `parent_path` | string | No | Workspace folder path (e.g., `/Workspace/Users/me/Genie`) |

### serialized_space JSON Structure

The `serialized_space` is a JSON string. Parse and stringify for API calls.

```json
{
  "layout": {
    "type": "GRID"
  },
  "components": [],
  "tableIdentifiers": [
    "main.sourabh_energy_workshop.gold_daily_consumption",
    "main.sourabh_energy_workshop.gold_customers_by_region"
  ],
  "sampleQuestions": [
    "What is the total consumption by region?",
    "Which region has the highest average usage?"
  ],
  "instructions": "Optional instructions for the Genie model."
}
```

### Fields in serialized_space

| Field | Type | Description |
|-------|------|-------------|
| `layout` | object | Layout config; `type: "GRID"` is typical |
| `components` | array | UI components (often empty for API-created spaces) |
| `tableIdentifiers` | array | Fully-qualified table names (catalog.schema.table) |
| `sampleQuestions` | array | Example questions to guide users |
| `instructions` | string | System instructions for query generation |

### Response

```json
{
  "space_id": "abc123...",
  "title": "Energy Analytics Genie",
  "description": "Natural language SQL exploration",
  "created_at": "2025-03-17T10:00:00Z"
}
```

### Example Python Call

```python
from databricks.sdk import WorkspaceClient
import json

w = WorkspaceClient()

payload = {
    "warehouse_id": "your-warehouse-id",
    "serialized_space": json.dumps({
        "layout": {"type": "GRID"},
        "components": [],
        "tableIdentifiers": ["main.sourabh_energy_workshop.gold_daily_consumption"],
        "sampleQuestions": ["What is total consumption by region?"],
        "instructions": "Use energy domain terminology."
    }),
    "title": "Energy Analytics",
    "parent_path": "/Workspace/Users/me/Genie"
}

resp = w.api_client.do("POST", "/api/genie/create_space", body=payload)
print(resp["space_id"])
```
