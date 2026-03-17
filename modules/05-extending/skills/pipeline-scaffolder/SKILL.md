---
name: pipeline-scaffolder
description: "Scaffolds medallion pipelines and creates them via the Databricks API. Generates SDP source files (bronze/silver/gold) from SQL templates and creates the pipeline. Use when bootstrapping energy data pipelines or automating pipeline deployment."
---

# Pipeline Scaffolder

Scaffold medallion (bronze/silver/gold) pipelines and create them via the Databricks Pipelines API. Generates SDP source files from SQL templates and deploys the pipeline.

## When to Use

- Bootstrapping new energy data pipelines
- Automating pipeline creation from templates
- Workshop demos requiring pre-built pipelines
- Standardizing medallion structure across projects

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Pipeline display name |
| `catalog` | Yes | Target Unity Catalog |
| `schema` | Yes | Target schema (e.g., `sourabh_energy_workshop`) |
| `source_path` | No | Volume path for raw data |
| `channel` | No | Update channel (CURRENT, PREVIEW) |

## Workflow

1. **Load templates** — bronze, silver, gold SQL from `assets/`
2. **Substitute placeholders** — catalog, schema, source path
3. **Write source files** — To local or workspace path
4. **Create pipeline** — POST /api/2.0/pipelines

## Script Usage

```bash
python scripts/scaffold_pipeline.py \
  --name "Energy Medallion" \
  --catalog main \
  --schema sourabh_energy_workshop \
  --source-path /Volumes/main/sourabh_energy_workshop/raw/
```

## Templates

| Template | Purpose |
|----------|---------|
| `assets/bronze-template.sql` | Raw ingestion (read_files, cloudFiles) |
| `assets/silver-template.sql` | Cleaned, validated data |
| `assets/gold-template.sql` | Aggregated business tables |

## Reference

- [databricks-spark-declarative-pipelines](../databricks-spark-declarative-pipelines/SKILL.md) — SDP patterns and best practices

## Prerequisites

- Databricks SDK
- Unity Catalog enabled
- Source data in Volume or cloud storage
