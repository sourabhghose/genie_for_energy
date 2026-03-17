# SmartGrid Analytics Platform — Dashboard

This folder contains the exported Lakeview dashboard JSON that can be imported into any Databricks workspace.

## Dashboard Pages

| Page | Widgets | Description |
|------|---------|-------------|
| **Executive Overview** | 3 KPIs, 2 charts, 2 pie charts | Total customers, MWh billed, solar adoption %, consumption by state, monthly revenue trend, customer type and rate plan distribution |
| **Grid Reliability** | 3 KPIs, 1 stacked bar, 1 table | Total outages, avg duration, meters affected, outages by cause/state, high-risk equipment (load > 85%) |
| **Outage Map** | 1 point map | Interactive Mapbox map with 5,000 outage locations colour-coded by cause and sized by affected meters |
| **Global Filters** | 1 multi-select | State filter affecting all pages |

## Import via REST API

```bash
# Read the dashboard JSON
DASHBOARD_JSON=$(cat smartgrid-analytics-platform.lvdash.json)

# Create the dashboard
databricks api post /api/2.0/lakeview/dashboards --json "{
  \"display_name\": \"SmartGrid Analytics Platform — Australia\",
  \"parent_path\": \"/Workspace/Users/$(databricks current-user me | jq -r .userName)\",
  \"warehouse_id\": \"YOUR_WAREHOUSE_ID\",
  \"serialized_dashboard\": $(echo "$DASHBOARD_JSON" | jq -c '.' | jq -Rs '.')
}"
```

## Import via Databricks Asset Bundles (DABs)

Add to your `databricks.yml`:

```yaml
resources:
  dashboards:
    smartgrid_analytics:
      display_name: "SmartGrid Analytics Platform — Australia"
      file_path: ./dashboard/smartgrid-analytics-platform.lvdash.json
      warehouse_id: ${var.warehouse_id}
```

## Prerequisites

The dashboard queries tables in `main.sourabh_energy_workshop`. Run `setup/generate_energy_data.py` first to create the data.
